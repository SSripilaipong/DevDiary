import React from "react";
import {Form, Input} from "antd";

const UsernameFormItem = (props) => {
    const { id } = props;

    return (<Form.Item
        name="username"
        label="ชื่อผู้ใช้"
        rules={[
            {
                required: true,
                whitespace: true,
                message: '',
            },
            {
                pattern: /^[a-zA-Z0-9]+$/,
                message: 'ตัวอักษรและตัวเลขเท่านั้น',
            },
            {
                min: 4,
                message: 'อย่างน้อย 4 ตัวอักษร',
            },
            {
                max: 16,
                message: 'ไม่เกิน 16 ตัวอักษร',
            },
        ]}
    >
        <Input id={id} />
    </Form.Item>);
}

export default UsernameFormItem;
