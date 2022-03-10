import React from "react";
import {Form, Input} from "antd";

type Props = {
    id: string
}

const EmailFormItem = (props: Props) => {
    const { id } = props;

    return (<Form.Item
        name="email"
        label="E-mail"
        rules={[
            {
                type: 'email',
                message: 'E-mail ไม่ถูกต้อง',
            },
            {
                required: true,
                message: '',
            },
        ]}
    >
        <Input id={id} />
    </Form.Item>);
}

export default EmailFormItem;
