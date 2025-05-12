#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8MultiArray
import hid
from usb_hid import usb_class

usb1 = usb_class.usb()

class HIDDevice_Send_Node(Node):
    def __init__(self):
        super().__init__('hid_device_node')
        
        # Parameters
        self.declare_parameter('vendor_id', 0x1302)
        self.declare_parameter('product_id', 0x1902)
        
        vid = self.get_parameter('vendor_id').value
        pid = self.get_parameter('product_id').value
        
        # Open device
        try:
            self.device = hid.Device(vid, pid)
            #self.device.open(vid, pid)
            self.get_logger().info(f"Opened HID device {vid:04x}:{pid:04x}")
        except Exception as e:
            self.get_logger().error(f"Failed to open HID device: {str(e)}")
            raise
        
        # Publisher 
        self.publisher = self.create_publisher(UInt8MultiArray, 'hid_data', 10)
        #self.subcriber = self.create_subscription(UInt8MultiArray, 'hid_data', self.read_data_callback, 10)   # Timer for reading
        
        self.timer = self.create_timer(0.5, self.send_data, self.read_data)
        #self.timer1 = self.create_timer(0.5, self.read_data)

    def send_data(self):
        try:
            if(usb1._PID_Start==1):
                data=[0x00]+[0x00]*63
                usb1._PID_KPs
                usb1._PID_KIs
                usb1._PID_KDs

                usb1._PID_Braker_Scalei
                usb1._PID_Error_Scalei

                data[3]=int((usb1._PID_duty+32768)%256)
                data[4]=int((usb1._PID_duty+32768)//256)
                data[5]=int(usb1._Measure_Encoder_1000ms//65536)
                data[6]=int((usb1._Measure_Encoder_1000ms%65536)//256)
                data[7]=int(usb1._Measure_Encoder_1000ms%256)

                data[9]=usb1._PID_RPM//256
                data[10]=usb1._PID_RPM%256
                data[11]=usb1._PID_DIR
                data[12]=usb1._PID_KPs//256
                data[13]=usb1._PID_KPs%256
                data[14]=usb1._PID_KIs//256
                data[15]=usb1._PID_KIs%256
                data[16]=usb1._PID_KDs//256
                data[17]=usb1._PID_KDs%256
                data[18]=usb1._PID_ENC_Resolution//256
                data[19]=usb1._PID_ENC_Resolution%256
                data[20]=usb1._PID_Max_RPM//256
                data[21]=usb1._PID_Max_RPM%256
                data[22]=usb1._PID_Scale_A//256
                data[23]=usb1._PID_Scale_A%256
                data[24]=usb1._PID_Scale_B//256
                data[25]=usb1._PID_Scale_B%256

                data[43]=(usb1._ENC_ERR+8388608)//65536
                data[44]=((usb1._ENC_ERR+8388608)%65536)//256
                data[45]=(usb1._ENC_ERR+8388608)%256
                data[46]=usb1._PID_PWM_Duty//256
                data[47]=usb1._PID_PWM_Duty%256
                data[48]=usb1._PID_ENC_1000ms//65536
                data[49]=(usb1._PID_ENC_1000ms%65536)//256
                data[50]=usb1._PID_ENC_1000ms%256
                
                data[55]=usb1._PID_Error_Scalei//256
                data[56]=usb1._PID_Error_Scalei%256
                data[57]=usb1._PID_Braker_Scalei//256
                data[58]=usb1._PID_Braker_Scalei%256
            else:
                self.get_logger().info("Khong gui du lieu")

            data_sent = bytes(data)
            self.device.write(data_sent)
            msg = UInt8MultiArray( )
            msg.data=data
            self.get_logger().info(f"Gui du lieu: {msg.data}")
            self.publisher.publish(msg)
        except Exception as e:
            self.get_logger().error(f"Gui du lieu that bai: {str(e)}")

    def read_data(self):
        data = self.device.read(64)
        if data:
            msg1 = UInt8MultiArray()
            msg1.data = data
            self.get_logger().info(f"Da nhan duoc data: {msg1.data}")
            self.publisher.publish(msg1)
        else:
            self.get_logger().warning("Khong co du lieu nhan duoc")
       
    def __del__(self):
        if hasattr(self, 'device'):
            self.device.close()

def main(args=None):
    rclpy.init(args=args)
    node = HIDDevice_Send_Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()