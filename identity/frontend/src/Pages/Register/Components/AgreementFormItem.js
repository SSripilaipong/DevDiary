import React from "react";
import {Checkbox, Form} from "antd";

const AgreementFormItem = (props) => {
    const { id } = props;

    return (<Form.Item
        name="agreement"
        valuePropName="checked"
        rules={[
            {
                validator: (_, value) =>
                    value ? Promise.resolve() : Promise.reject(new Error('อ่านเงื่อนไขการให้บริการ')),
            },
        ]}
        {...props.tailFormItemLayout}
    >
        <Checkbox id={id}>
            ยอมรับ<a href="">เงื่อนไขการให้บริการ</a>
        </Checkbox>
    </Form.Item>);
}

export default AgreementFormItem