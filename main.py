from PIL import Image
import numpy as np
from stl import mesh
from io import BytesIO
import requests

request_url = 'https://wms.geonorge.no/skwms1/wms.hoyde-dom?' \
           'SERVICE=WMS&' \
           'VERSION=1.3.0&' \
           'REQUEST=GetMap&' \
           'FORMAT=image/png&' \
           'TRANSPARENT=false&' \
           'LAYERS=DOM:None&' \
           'CRS=EPSG:102100&' \
           'STYLES=&' \
           'WIDTH=900&' \
           'HEIGHT=1000&' \
           'BBOX= -41608.792735, 7959036.255282, 3441415.562179, 11525516.916074'


response = requests.get(request_url, verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
print(f"HTTP response status code = {response.status_code}")

grey_img = Image.open(BytesIO(response.content)).convert('L')
transposed  = grey_img.transpose(Image.ROTATE_180)
grey_img.show()

max_size=(300, 200)
max_height=10
min_height=0

#height=0 for minPix
#height=maxHeight for maxPIx

grey_img.thumbnail(max_size)
imageNp = np.array(grey_img)
maxPix=imageNp.max()
minPix=imageNp.min()

print(f"max:{imageNp.max()}")

print(imageNp)
(ncols,nrows)=grey_img.size

vertices=np.zeros((nrows,ncols,3))

for x in range(0, ncols):
  for y in range(0, nrows):
    pixelIntensity = imageNp[y][x]
    z = (pixelIntensity * max_height) / maxPix
    #print(imageNp[y][x])
    vertices[y][x]=(x, y, z)

faces=[]

for x in range(0, ncols - 1):
  for y in range(0, nrows - 1):
    # create face 1
    vertice1 = vertices[y][x]
    vertice2 = vertices[y+1][x]
    vertice3 = vertices[y+1][x+1]
    face1 = np.array([vertice1,vertice2,vertice3])

    # create face 2
    vertice1 = vertices[y][x]
    vertice2 = vertices[y][x+1]
    vertice3 = vertices[y+1][x+1]

    face2 = np.array([vertice1,vertice2,vertice3])

    faces.append(face1)
    faces.append(face2)

print(f"number of faces: {len(faces)}")
facesNp = np.array(faces)
# Create the mesh
surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        surface.vectors[i][j] = facesNp[i][j]
# Write the mesh to file "cube.stl"
surface.save('surface.stl')
print(surface)