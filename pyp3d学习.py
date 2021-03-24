import pyp3d as p3d
import pretty_errors

box1=p3d.Box(p3d.Vec3(0,0,0),p3d.Vec3(0,0,3000),p3d.Vec3(1,0,0),p3d.Vec3(0,1,0),3000,5000,1000,1000).color(1,1,0,0.5)
p3d.createGeometry(box1)

