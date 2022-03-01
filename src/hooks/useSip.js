import React, { useContext } from 'react';

import { SipContext } from '../contexts/SipProvider';

const useSip = () => {
    const ua = useContext(SipContext)
    if (ua === undefined)
        throw new Error('fail to setup SIP')
    return ua
};

export default useSip;