import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.ndimage
import scipy.sparse.linalg
from scipy import sparse
def load(url):
  (fname,_) = urllib.request.urlretrieve(url)
  try:
    data=plt.imread(fname)
  except:
    (fname,_) = urllib.request.urlretrieve(url+'.png')
    data=plt.imread(fname)
  M = np.max(data)
  data = data/M
  if data.shape[2]==4:
    d = data
    data = np.zeros((d.shape[0],d.shape[1],3))
    alpha = d[:,:,3]
    if(np.min(alpha)<0.95):
      print("Warning: the image has a nontrivial alpha channel.\nYou probably forgot to clear the background to white.")
    for k in range(3):
      data[:,:,k] = d[:,:,k]*alpha+(1-alpha)
  E = np.max(np.abs(data[:,:,0]-data[:,:,1])+
      np.abs(data[:,:,2]-data[:,:,1])+
      np.abs(data[:,:,0]-data[:,:,2]))
  assert E<0.1, "Image should be black-and-white"
  m = data.shape[0]
  n = data.shape[1]
  assert 100<=m and m<=200, "Image should be between 100 and 200 pixels tall"
  assert 100<=n and n<=200, "Image should be between 100 and 200 pixels wide"
  G = np.zeros((m+2,n+2))
  G[1:-1,1:-1] = (data[:,:,0]<0.25)+0
  F = np.sum(G)/(G.shape[0]*G.shape[1])
  assert F>0.1, "Image should have at least 10% dark pixels"
  assert F<0.9, "Image should have at most 90% dark pixels"
  H = np.copy(G)
  dirs = [[1,0],[-1,0],[0,1],[0,-1]]
  for k in range(1):
    flags = np.zeros(H.shape)
    for j in range(4):
      dx = dirs[j][0]
      dy = dirs[j][1]
      x1 = 1+dx
      x2 = 1+m+dx
      y1 = 1+dy
      y2 = 1+n+dy
      foo = H[x1:x2,y1:y2]
      flags[1:-1,1:-1] = flags[1:-1,1:-1] + foo
    H = H*(flags>0)
  (labeled, nr_objects) = scipy.ndimage.label(H)
  assert nr_objects==1, "Image should consist of 1 component"
  G1 = np.reshape(G,((m+2)*(n+2),))
  W = np.where(G1)
  G1[W] = range(0,len(W[0]))
  G = np.reshape(G1,(m+2,n+2)).astype(int)
  
  plt.imshow(data)
  plt.show()
  return G
def discrete_2d_Laplacian(G):
  G = G.astype(int)
  G_ = np.reshape(G,np.prod(G.shape)); 
  G_ = np.sort(G_[np.where(G_>0)])
  assert np.array_equal(G_,np.array(range(1,len(G_)+1))), "The grid must enumerate consecutive vertices.\nSee the Section on the 2d Laplacian in the handout."
  assert (
    len(np.where(G[0,:]!=0)[0])==0
    and len(np.where(G[-1,:]!=0)[0])==0
    and len(np.where(G[:,0]!=0)[0])==0
    and len(np.where(G[:,-1]!=0)[0])==0
    ), "The perimeter of the grid must be 0"
  N = np.max(G)
  m = G.shape[0]-2
  n = G.shape[1]-2
  L = 4*sparse.eye(N,N)
  dirs = [[0,1],[0,-1],[1,0],[-1,0]]
  for j in range(4):
    dx = dirs[j][0]
    dy = dirs[j][1]
    G0 = np.reshape(G[1:-1,1:-1],(m*n,))
    G1 = np.reshape(G[1+dx:m+1+dx,1+dy:n+1+dy],(m*n,))
    W = np.where(G0*G1>0)
    G0 = G0[W]
    G1 = G1[W]
    Z = np.ones((len(G0),))
    L = L - sparse.csc_matrix((Z,(G0-1,G1-1)),shape=(N,N))
  return L
def viewsol(G,u):
  G1 = np.reshape(G,(G.shape[0]*G.shape[1],))
  W = np.where(G1)
  C = np.zeros(G1.shape[0])
  C[W] = u
  C = np.reshape(C,G.shape)
  plt.imshow(C)
  plt.colorbar()
  H = np.ones(G1.shape[0])
  H[np.where(G1>0)] = 0.0
  Z = np.ones([G.shape[0],G.shape[1],4])
  Z[:,:,3] = np.reshape(H,G.shape)
  plt.imshow(Z)
  plt.show()
def solve(A,b):
  if(scipy.sparse.issparse(A)):
    return sparse.linalg.spsolve(A,b)
  return np.linalg.solve(A,b)
def I(n):
    return sparse.eye(n)
def norm(a):
  return np.linalg.norm(a)
def randn(n):
  return np.random.randn(n)
def array(x):
  return np.array(x)
def ones(n):
  return np.ones(n)
def dot(u,v):
  return np.dot(u,v)
