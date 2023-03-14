#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os

# Load the request module
import urllib.request

# Import SSL which we need to setup for talking to the HTTPS server
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# In[27]:


files = os.listdir('birme-200x200')# img.<tab>
import matplotlib.pyplot as plt
import numpy as np

print(os.path.join('birme-200x200', files[0]))
plt.imread(os.path.join('birme-200x200', files[0]))

files = [os.path.join('birme-200x200', file_i)
 for file_i in os.listdir('birme-200x200')
 if '.jpg' in file_i]

# There should be 100 files, with the last one being number 99

img = plt.imread(files[14])

print(img)


# In[28]:


plt.imshow(img)


# In[29]:


img.shape


# In[30]:


plt.imshow(img[:, :, 1], cmap='gray')


# In[31]:


plt.imshow(img[:, :, 2], cmap='gray') # Blue Channel


# In[34]:


imgs = [plt.imread(files[file_i])
        for file_i in range(14)]


# In[37]:


plt.imshow(imgs[12])


# In[38]:


imgs[0].shape


# In[39]:


data = np.array(imgs) # make 'data' = our numpy array
data.shape
print(data.shape)
print("The shape of our new 'data' object is a 'batch' of 100 images, with a height of 218, width of 178, and 3 colour channels")
print("If your images aren't all the same size to begin with, then this won't work!")


# In[40]:


mean_img = np.mean(data, axis=0) # This is the mean of the 'batch' channel
plt.imshow(mean_img.astype(np.uint8))
print("look at this average person")


# In[41]:


std_img = np.std(data, axis=0)
plt.imshow(std_img.astype(np.uint8))
print("This is the standard deviation - the variance of the mean")


# In[42]:


plt.imshow(np.mean(std_img, axis=2).astype(np.uint8)) # Mean of all colour channels
print("Mean of all colour channels")


# In[43]:


flattened = data.ravel()
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.ravel.html
print(data[:1])
print(flattened[:10])


# In[44]:


plt.hist(flattened.ravel(), 255)


# In[45]:


plt.hist(mean_img.ravel(), 255)


# In[46]:


bins = 20
fig, axs = plt.subplots(1, 3, figsize=(12, 6), sharey=True, sharex=True)
axs[0].hist((data[0]).ravel(), bins)
axs[0].set_title('img distribution')
axs[1].hist((mean_img).ravel(), bins)
axs[1].set_title('mean distribution')
axs[2].hist((data[0] - mean_img).ravel(), bins)
axs[2].set_title('(img - mean) distribution')


# In[47]:


fig, axs = plt.subplots(1, 3, figsize=(12, 6), sharey=True, sharex=True)
axs[0].hist((data[0] - mean_img).ravel(), bins)
axs[0].set_title('(img - mean) distribution')
axs[1].hist((std_img).ravel(), bins)
axs[1].set_title('std deviation distribution')
axs[2].hist(((data[0] - mean_img) / std_img).ravel(), bins)
axs[2].set_title('((img - mean) / std_dev) distribution')


# In[48]:


axs[2].set_xlim([-150, 150])
axs[2].set_xlim([-100, 100])
axs[2].set_xlim([-50, 50])
axs[2].set_xlim([-10, 10])
axs[2].set_xlim([-5, 5])


# In[49]:


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


# In[50]:


x = np.linspace(-3.0, 3.0, 100)

# Immediately, the result is given to us.  An array of 100 numbers equally spaced from -3.0 to 3.0.
print(x)

# We know from numpy arrays that they have a `shape`, in this case a 1-dimensional array of 100 values
print(x.shape)

# and a `dtype`, in this case float64, or 64 bit floating point values.
print(x.dtype)


# In[51]:


x = tf.linspace(-3.0, 3.0, 100)
print(x)


# In[52]:


g = tf.get_default_graph()


# In[53]:


[op.name for op in g.get_operations()]


# In[54]:


g.get_tensor_by_name('linspace/Slice' + ':0')


# In[55]:


# We're first going to create a session:
sess = tf.Session()

# Now we tell our session to compute anything we've created in the tensorflow graph.
computed_x = sess.run(x)
print(computed_x)

# Alternatively, we could tell the previous Tensor to evaluate itself using this session:
computed_x = x.eval(session=sess)
print(computed_x)

# We can close the session after we're done like so:
sess.close()


# In[56]:


sess = tf.Session(graph=g)
sess.close()


# In[57]:


g2 = tf.Graph()


# In[58]:


sess = tf.InteractiveSession()
x.eval()


# In[59]:


# We can find out the shape of a tensor like so:
print(x.get_shape())

# %% Or in a more friendly format
print(x.get_shape().as_list())


# In[60]:


# The 1 dimensional gaussian takes two parameters, the mean value, and the standard deviation, which is commonly denoted by the name sigma.
mean = 0.0
sigma = 1.0

# Don't worry about trying to learn or remember this formula.  I always have to refer to textbooks or check online for the exact formula.
z = (tf.exp(tf.negative(tf.pow(x - mean, 2.0) /
                   (2.0 * tf.pow(sigma, 2.0)))) *
     (1.0 / (sigma * tf.sqrt(2.0 * 3.1415))))


# In[61]:


res = z.eval()
plt.plot(res)
# if nothing is drawn, and you are using ipython notebook, uncomment the next two lines:
#%matplotlib inline
#plt.plot(res)


# In[62]:


# Let's store the number of values in our Gaussian curve.
ksize = z.get_shape().as_list()[0]

# Let's multiply the two to get a 2d gaussian
z_2d = tf.matmul(tf.reshape(z, [ksize, 1]), tf.reshape(z, [1, ksize]))

# Execute the graph
plt.imshow(z_2d.eval())


# In[ ]:




