import React from "react";
import {Form, Input} from "antd";

type Props = {
    id: string
}

const PasswordConfirmFormItem = (props: Props) => {
    const { id } = props;

    return (<Form.Item
        name="confirm"
        label="ยืนยันรหัสผ่าน"
        dependencies={['password']}
        hasFeedback
        rules={[
            {
                required: true,
                message: '',
            },
            ({ getFieldValue }) => ({
                validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                    }
                    return Promise.reject(new Error('รหัสผ่านไม่ตรงกัน'));
                },
            }),
        ]}
    >
        <Input.Password id={id}/>
    </Form.Item>);
}

export default PasswordConfirmFormItem;
