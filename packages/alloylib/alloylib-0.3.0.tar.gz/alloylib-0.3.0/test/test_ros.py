import pytest
#test if ros exist
import alloy.ros
try:
    from geometry_msgs.msg import(
        Point,
        Pose,
        Transform,
        TransformStamped,
        PoseStamped
    )
except (ImportError, ModuleNotFoundError):
    pytest.skip("skipping ROS tests because ROS is not installed.", allow_module_level=True)


def test_point_transform():
    p = Point(x=1,y=2,z=3)
    t = Transform()
    t.rotation.w = 1 # the default transform isn't proper
    pt = alloy.ros.do_transform_point(t,p)
    assert pt.x == p.x
    assert pt.y == p.y
    assert pt.z == p.z

    # try distance transform
    t2 = Transform()
    t2.rotation.w = 1 # the default transform isn't proper
    t2.translation.x = 10
    t2.translation.y = 20
    t2.translation.z = 30
    pt = alloy.ros.do_transform_point(t2,p)
    assert pt.x == p.x + t2.translation.x 
    assert pt.y == p.y + t2.translation.y 
    assert pt.z == p.z + t2.translation.z 

    # try rotation transform
    t3 = Transform()
    t3.rotation.w = 0.7071068
    t3.rotation.x = 0.7071068
    pt = alloy.ros.do_transform_point(t3,p)
    assert pt.x == pytest.approx(p.x)
    assert pt.y == pytest.approx(p.z * -1)
    assert pt.z == pytest.approx(p.y)  

    # try rotation + distance transform
    t3.translation.x = -10
    t3.translation.y = -20
    t3.translation.z = -30
    pt = alloy.ros.do_transform_point(t3,p)
    assert pt.x == pytest.approx(p.x + t3.translation.x)
    assert pt.y == pytest.approx(p.z * -1 + t3.translation.y)
    assert pt.z == pytest.approx(p.y + t3.translation.z)  

def test_pose_transform():
    p = Pose()
    p.position.x = 10
    p.position.y = 20 
    p.position.z = 30
    p.orientation.w = 1
    t = Transform()
    t.rotation.w = 1
    pt = alloy.ros.do_transform_pose(t, p)
    assert pt.position.x == p.position.x
    assert pt.position.y == p.position.y
    assert pt.position.z == p.position.z
    assert pt.orientation.w == p.orientation.w
    assert pt.orientation.z == pt.orientation.y == pt.orientation.x == 0

    # try rotation transform
    t.rotation.w = 0.7071068
    t.rotation.x = 0.7071068
    pt = alloy.ros.do_transform_pose(t,p)
    assert pt.position.x == pytest.approx(p.position.x)
    assert pt.position.y == pytest.approx(p.position.z * -1)
    assert pt.position.z == pytest.approx(p.position.y)  
    assert pt.orientation.w == pytest.approx(t.rotation.w) 
    assert pt.orientation.x == pytest.approx(t.rotation.x) 
    assert pt.orientation.z == pt.orientation.y == 0    

    p.orientation.w = 0.7071068
    p.orientation.x = 0.7071068
    pt = alloy.ros.do_transform_pose(t,p)
    assert pt.position.x == pytest.approx(p.position.x)
    assert pt.position.y == pytest.approx(p.position.z * -1)
    assert pt.position.z == pytest.approx(p.position.y)  
    assert pt.orientation.x == pytest.approx(1) 
    assert pt.orientation.z == pytest.approx(0)    
    assert pt.orientation.y == pytest.approx(0)    
    assert pt.orientation.w == pytest.approx(0)    

def is_empty_pose(p: Pose):
    assert p.position.x == 0
    assert p.position.y == 0
    assert p.position.z == 0
    assert p.orientation.w == 0
    assert p.orientation.x == 0
    assert p.orientation.y == 0
    assert p.orientation.z == 0

def test_to_pose_success():
    # test empty + types 
    is_empty_pose(alloy.ros.to_pose(Transform()))
    is_empty_pose(alloy.ros.to_pose(Pose()))
    is_empty_pose(alloy.ros.to_pose(PoseStamped()))
    is_empty_pose(alloy.ros.to_pose(TransformStamped()))

    # test some converts
    t = Transform()
    t.rotation.w = 0.7071068
    t.rotation.x = 0.7071068
    t.translation.y = 10
    t.translation.z = 5
    p = alloy.ros.to_pose(t)
    assert p.position.x == t.translation.x
    assert p.position.y == t.translation.y
    assert p.position.z == t.translation.z
    assert p.orientation.x == t.rotation.x
    assert p.orientation.y == t.rotation.y
    assert p.orientation.z == t.rotation.z
    assert p.orientation.w == t.rotation.w



def test_to_pose_failed():
    assert alloy.ros.to_pose("x") is None
    assert alloy.ros.to_pose(None) is None
