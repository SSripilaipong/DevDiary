import React from 'react';
const RemoteRegisterPage = React.lazy(() => import('identity/Register')
    .then(module => ({default: module.RegisterPage})));

export default function RegisterPage() {
    return (<React.Suspense fallback='Loading'>
        <RemoteRegisterPage />
    </React.Suspense>);
}
