import React from "react";
import {Form, Input} from "antd";

type Props = {
    id: string
}

const PasswordFormItem = (props: Props) => {
    const { id } = props;

    return (<Form.Item
        name="password"
        label="รหัสผ่าน"
        rules={[
            {
                required: true,
                message: '',
            },
            {
                min: 8,
                message: 'อย่างน้อย 8 ตัวอักษร',
            },
            {
                max: 64,
                message: 'ต้องไม่เกิน 64 ตัวอักษร',
            },
            {
                pattern: new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])"),
                message: 'ต้องมีตัวพิมพ์เล็ก ตัวพิมพ์ใหญ่ และตัวเลข',
            }
        ]}
        hasFeedback
    >
        <Input.Password id={id} />
    </Form.Item>);
}

export default PasswordFormItem;
