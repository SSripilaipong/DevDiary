import React from "react";
import { notification } from 'antd';

const showSuccessNotification = () => {
    notification.success({
        message: "สมัครสมาชิกสำเร็จ",
        description: "ระบบจะส่ง email ยืนยันการสมัครสมาชิกไปในไม่ช้า\nจะสามารถใช้งานระบบได้หลังจากทำการยืนยันการสมัครสมาชิกแล้ว",
        placement: "topLeft",
    });
};

export default showSuccessNotification;
