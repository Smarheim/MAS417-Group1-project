from PIL import Image
import numpy as np
from stl import mesh
from io import BytesIO
import requests

# Example BBOX values: 56.4897 -7.04219 72.2495 37.4864


class MapData:

    # Attributes
    BBOX_Values = input('Enter BBOX values separated by space:')
    BBOX = BBOX_Values.split()

    for i in range(len(BBOX)):
        BBOX[i] = str(BBOX[i])


BBOX = ', '.join(MapData.BBOX)

request_url = 'https://wms.geonorge.no/skwms1/wms.hoyde-dom?' \
           'SERVICE= WMS&' \
           'VERSION=1.3.0&' \
           'REQUEST=GetMap&' \
           'FORMAT=image/png&' \
           'TRANSPARENT=false&' \
           'LAYERS=DOM:None&' \
           'CRS=EPSG:4258&' \
           'STYLES=&' \
           'WIDTH=825&' \
           'HEIGHT=617&' \
           'BBOX=' f'{BBOX}' \

response = requests.get(request_url, verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
print(f"HTTP response status code = {response.status_code}")

grey_img = Image.open(BytesIO(response.content)).convert('L')
transposed  = grey_img.transpose(Image.ROTATE_180)
grey_img.show()

max_size=(900, 700)
max_height=10
min_height=0

# height=0 for minPix
# height=maxHeight for maxPIx

grey_img.thumbnail(max_size)
imageNp = np.array(grey_img)
maxPix = imageNp.max()
minPix = imageNp.min()

print(f"max:{imageNp.max()}")

print(imageNp)
(ncols,nrows) = grey_img.size

vertices=np.zeros((nrows,ncols,3))

for x in range(0, ncols):
  for y in range(0, nrows):
    pixelIntensity = imageNp[y][x]
    z = (pixelIntensity * max_height) / maxPix
    # print(imageNp[y][x])
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