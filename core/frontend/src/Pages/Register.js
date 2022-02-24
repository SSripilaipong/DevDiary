import React from 'react';
const { RegisterPage: RemoteRegisterPage } = React.lazy(() => import('identity/Register'));

export default function RegisterPage() {
    return (<React.Suspense fallback='Loading'>
        <RemoteRegisterPage />
    </React.Suspense>);
}
