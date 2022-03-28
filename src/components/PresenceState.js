import React from 'react'
import { useTranslation } from 'react-i18next'
import styled from 'styled-components'

export default function PresenceState({ state }) {
    const { t } = useTranslation()
    switch (state) {
        case 100:
            return <Wrap className='statusOffline'>{t('offline')}</Wrap>
        case 101:
            return <Wrap className='statusOnHoding'>{t('afterTreatment')}</Wrap>
        case 102:
            return <Wrap className='statusOnHoding'>{t('onHoding')}</Wrap>
        case 103:
            return <Wrap className='statusIncomingCall'>{t('incomingCall')}</Wrap>
        case 104:
            return <Wrap className='statusInACall'>{t('inACall')}</Wrap>
        default:
            return <Wrap className='statusOffline'>{t('offline')}</Wrap>
    }
     {/* {status === "on Hoding" ?
                                            <span className='statusOnHoding'>{t('onHoding')}</span>
                                            :
                                            status === 'Acceptable' ?
                                                <span className='statusAcceptable'>{t('acceptable')}</span>
                                                :
                                                status !== 'after-Treatment' ?
                                                    <span className='statusOnHoding'>{t('afterTreatment')}</span>
                                                    :
                                                    status === 'after-Treatment' ?
                                                        <span className='statusOnHodingInTransferredCall'>{t('onHoding')} ({t('in transferred call')})</span>
                                                        :
                                                        status === 'after-Treatment' ?
                                                            <span className='statusIncomingCall'>{t('incomingCall')}</span>
                                                            :
                                                            <span className='statusInACall'>{t('inACall')}</span>

                                        } */}
}

const Wrap = styled.span`
    /* .statusOffline{
        font-size: calc(0.5vw + 0.6vh);
        color: #707070;
        background-color: #ECECEC;
        border: 1px solid #707070;
        padding: 3px 10px 3px 10px;
        border-radius: 100px;
    } */
    /* .statusOnHoding {
        font-size: calc(0.5vw + 0.6vh);
        color: #FFB800;
        background-color: #FFF7E1;
        border: 1px solid #FFB800;
        padding: 3px 10px 3px 10px;
        border-radius: 100px;
    }
    .statusOnHodingInTransferredCall {
        font-size: calc(0.6vh + 0.5vw);
        color: #FFB800;
        background-color: #FFF7E1;
        border: 1px solid #FFB800;
        padding: 3px 10px 3px 10px;
        border-radius: 50px;
    }
    .statusAcceptable {
        font-size: calc(0.5vw + 0.6vh);
        color: #056FED;
        background-color: #E2EFFF;
        border: 1px solid #056FED;
        padding: 3px 10px 3px 10px;
        border-radius: 50px;
    }

    .statusIncomingCall {
        font-size: calc(0.5vw + 0.6vh);
        color: #009944;
        background-color: #E7FFF2;
        border: 1px solid #009944;
        padding: 3px 10px 3px 10px;
        border-radius: 50px;
    }
    .statusInACall {
        font-size: calc(0.5vw + 0.6vh);
        color: #E30000;
        background-color: #FFE1E1;
        border: 1px solid #E30000;
        padding: 3px 10px 3px 10px;
        border-radius: 50px;
    } */
`
