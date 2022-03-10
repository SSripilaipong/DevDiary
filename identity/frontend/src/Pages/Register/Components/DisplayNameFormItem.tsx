import React from "react";
import {Form, Input} from "antd";

type Props = {
    id: string
}

const DisplayNameFormItem = (props: Props) => {
    const { id } = props;

    return (<Form.Item
        name="displayName"
        label="ชื่อ display"
        rules={[{ required: true, message: '', whitespace: true }]}
    >
        <Input id={id} />
    </Form.Item>);
}

export default DisplayNameFormItem;
