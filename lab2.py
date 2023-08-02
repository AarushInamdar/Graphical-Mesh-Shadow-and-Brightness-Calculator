{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Lab 2\n",
    "___\n",
    "## To submit\n",
    "Go to the file tab, and download this notebook as .py. Make sure this file is named lab2.py, and submit it to Gradescope.\n",
    "___\n",
    "1. In computer graphics, we represent physical objects in form of connected triangles. Each triangle represent part of surface of the object. Each triangle has 3 vertices, that each vertex is a point in 3D space. In fact, triangle edges connect these 3D points in a way that the triangles look like the  surface of the object. For example a simple cube can be created by 8 vertices and 12 triangles (2 triangle per side). We can create very approximate very complicated surfaces with triangle mesh (like the terrain).\n",
    "\n",
    "<img src=\"images/cube_triangle.png\">\n",
    "\n",
    "<img src=\"images/terrain_triangle.jpg\">\n",
    "\n",
    "We know that in 3-dim space we can represent a point with a 3-dim vector. That  vector starts from the origin (0,0,0) and ends at that point. So, each triangle in a mesh is basically composed of three vectors.\n",
    "\n",
    "2. A simple way to store a triangular mesh in computer is keeping 2 matrices: one for vertices, and another one for triangles. Here we represent the above 2D triangular mesh with two matrices: vertex matrix (V) and triangles matrix (F). The vertex matrix (V) is an $n \\times 3$ matrix that represents $n$ vertices that each vertex is a row of this matrix which is a point in 3D space. The triangle matrix (F) is an $m \\times 3$ matrix that represents $m$ triangles that each triangle is a row of this matrix which is the index of vertices that form a triangle. For example the V and F matrices for this mesh is:\n",
    "\n",
    "<img src=\"images/simple_mesh.jpg\">\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "tags": []
   },
   "outputs": [],
   "source": [
    "V = np.array([\n",
    "    [0, 0, 0],\n",
    "    [1, 0, 0],\n",
    "    [1, 1, 0],\n",
    "    [0, 1, 0]])\n",
    "\n",
    "F = np.array([\n",
    "    [0, 1, 2],\n",
    "    [0, 2, 3]])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In the above example we have 4 vertices ($n = 4$) and 2 triangle ($m = 2$). Triangle 0 (row 0 of matrix F) is made of vertices 0, 1, and 2. Note that these numbers are the order of this triangle's vertices in the matrix V. It is customary that to represent each tringle with its vertices in counter-clockwise order. That is if we replce the first row of matrix F with 1, 2, 0 or 2, 0, 1, they all are correct way of representing triangle 0.\n",
    "\n",
    "3. We know cross product of two vectors is a vector perpendicular to both vectors and its size is proportional to the size of the two vectors and $sin$ of the angle between them:\n",
    "\n",
    "$a \\times b = \\left\\lVert a \\right\\rVert \\left\\lVert b \\right\\rVert \\sin(\\theta)$\n",
    "\n",
    "The direction of $a \\times b$ follows the right-hand rule. That is if you try to move the four fingers of your right hand from $a$ to $b$, then your thumb shows the direction of $a \\times b$ as shown below.\n",
    "\n",
    "<img src=\"images/right_hand_cross.png\">\n",
    "\n",
    "Obviously if you change the order of $a$ and $b$, the result $b \\times a$ will be in the opposite direction of $a \\times b$. Now let's look back in a sample triangle from a mesh. Suppose a triangle is made of three vertices, $v_0, v_1,$ and $v_2$ in counter clock-wise order. And let's name the three edges as $e_{0,1}, e_{1,2},$ and $e_{2,0}$, where $e_{i,j}$ is an  edge starting from $v_i$ and ending at $v_j$. Following shows a sample triangle with its vertices and edges.\n",
    "\n",
    "<img src=\"images/edges_triangle.jpg\">\n",
    "\n",
    "Now try applying the right-hand rule on two consecutive edges (say $e_{0,1} \\times e_{1,2}$ on your monitor). Your will see that your thumb will direct from your monitor to yourself. This direction is the direction of normal vector of this triangle. Using this method you can calculate the normal vector for each triangle in a triangular mesh. Since the normal vector of a triangle should be independent of the area of triangle, we always make the normal vector to be a unit vector. "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Exercise 1\n",
    "You should complete the following python function named \"calc_normal\" that takes vertices (V) and triangles (F) of an input triangular mesh and return a matrix that its i-th row is the normal vector of i-th triangle in matrix F. Note that the normal vector should be a unit vector. \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[0., 0., 1.],\n",
       "       [0., 0., 1.]])"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "def calc_normal(V: np.array, F: np.array) -> np.array:\n",
    "    m,_ = F.shape\n",
    "    N = np.zeros((m, 3))\n",
    "    \n",
    "    for i in range(m):\n",
    "        vector_1 = V[F[i][0]]\n",
    "        vector_2 = V[F[i][1]]\n",
    "        vector_3 = V[F[i][2]]\n",
    "        \n",
    "        u = vector_2 - vector_1\n",
    "        v = vector_3 - vector_1\n",
    "        \n",
    "        n = np.cross(u, v)\n",
    "        n = n/ np.linalg.norm(n)\n",
    "        \n",
    "        N[i] = n\n",
    "        \n",
    "    return N\n",
    "calc_normal(V,F)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "4. In computer graphics, creating images (frames) from a scene (objects and light sources) is called \"Rendering\". We see objects since they reflect light to our eyes. The light ray reaches the object surface from a light source and makes the surface visible. One of the form of light sources is a point light source. That is we assume there is a light source somewhere in 3D space, represented as a 3-dim vector, and it shines the rays of light to all directions. \n",
    "\n",
    "<img src=\"images/point light-1.png\">\n",
    "\n",
    "For matte materials the brightness of a surface is proportional to the angle between the normal direction of the surface to the light ray from the light source. That means the surface is brightest if the light ray is in the same direction of surface normal. In this assignment, for sake of simplicity, we find a single ray from each triangle to the light source. That single ray is a vector from the center of the triangle $(b)$ to the light source $(s)$.\n",
    "\n",
    "<img src=\"images/light_rendering.jpg\">\n",
    "\n",
    "The center of a triangle (barycentric point) can easily be calculated as the center of mass of a triangle. We don't want to go into details on this, but you can simply calculate the center of each triangle using the following formula:\n",
    "\n",
    "$b = \\frac{1}{3} (v_0 + v_1 + v_2)$\n",
    "\n",
    "It is a linear combination of three vertices of the triangle. Once you calculate the center of a triangle, you can then calculate the vector that starts from that point to the light source as:\n",
    "\n",
    "$l = s - b$\n",
    "\n",
    "The dot product between the two vectors $\\hat{n}$ (unit vector of normal of triangle) and $\\hat{l}$ (unit vector from triangle center to light source) is equal to cos of the angle between them. We know $\\cos(\\theta)$ has a value between -1 and 1. It is 1, when the angle is 0 degrees, and it is 0 when the angle is 90 degrees. That makes sense as you can imagine a surface is not lit if a point light source is parallel to the surface.\n",
    "\n",
    "The interesting part is when $\\cos(\\theta)$ is negative the angle is greater than 90 degrees. It means the light ray is being emitted to the back side of the triangle (for example the light is in the other side of cube, so this side doesn't get any light and is dark).\n",
    "\n",
    "In this exercise you should calculate the brightness of each triangle in mesh given a light source coordinate. The brightness is:\n",
    "\n",
    "$brightness = \\hat{n} \\cdot \\hat{l}$\n",
    "\n",
    "if the angle between $\\hat{n}$ and $\\hat{l}$ is less than 90 degrees. The brightness should be zero if that angle is greater than 90 degrees."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Exercise 2 \n",
    "You should complete the python function named \"calc_brightness\" that takes the two matrices of vertices (V) and triangles (F) which together represent a triangular mesh along with a 3D point that represent the location of light source and return a vector (numpy array), that its i-th element in output vector is the brightness of the i-th triangle in matrix F. Note that the brightness of each triangle should be an scalar between 0 to 1.\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "def calc_brightness(V: np.array, F: np.array, s: np.array) -> np.array:\n",
    "    N = calc_normal(V, F)  # Assuming calc_normal is already defined\n",
    "    \n",
    "    m,_ = F.shape\n",
    "    brightness = np.zeros(m)\n",
    "    \n",
    "    for i in range(m):\n",
    "        Ver_1 = V[F[i,0]]\n",
    "        Ver_2 = V[F[i,1]]\n",
    "        Ver_3 = V[F[i,2]]\n",
    "        \n",
    "        b = (1/3) * (Ver_1 + Ver_2 + Ver_3)\n",
    "        l = s - b\n",
    "        \n",
    "        n = N[i]/np.linalg.norm(N[i])\n",
    "        b = (1/np.linalg.norm(l))\n",
    "        brightness[i] = np.dot(n, b)\n",
    "        \n",
    "        if brightness[i] < 0:\n",
    "            brightness[i] = 0\n",
    "            \n",
    "    return brightness\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "5. In this lab assignment you wrote functions to perform very basic rendering calculations using two simple but fundamental operations in linear algebra (dot product and cross product of vectors). Your function calculates the brightness of each tringle depending on how it is lit by a point light source. For example you can see how the brightness of each triangle is rendered differently for the following image.\n",
    "\n",
    "<img src=\"images/point_source_rendered_mesh.png\">\n",
    "\n",
    "In many computer graphics applications (e.g. computer games), such operations should take place for thousands of triangles per frame. Unlike your Python functions that perform these operations on CPU, computer graphic applications utilize the specific hardware on computer called GPU, performing all these calculations on triangles and vertices in parallel to increase the fps (frames per second). "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
