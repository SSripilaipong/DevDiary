import React from 'react';
const IdentityButton = React.lazy(() => import('identity/Button'));

export default function HomePage() {
    return (<div>
        <div>This is Home Page</div>
        <React.Suspense fallback='Loading Button'>
            <IdentityButton/>
        </React.Suspense>
    </div>);
}
