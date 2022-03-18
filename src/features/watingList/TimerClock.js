import React, { useState, useEffect, useMemo, useRef } from 'react';



const TimerClock = (props) => {

    const [clock, setClock] = useState('');
    const intervalId = useRef();

    useEffect(() => {
        timer();
        restartInterval();

        return () => {
            if (intervalId.current) {
                clearInterval(intervalId.current);
            }
        }
    }, []);

    useEffect(() => {
        timer();
        restartInterval();
    }, [props.longestWait]);

    const restartInterval = () => {
        if(intervalId.current){
            clearInterval(intervalId.current);
        }
        intervalId.current = setInterval(timer, 1000);
    }

    const timer = () => {
        let longgestWaitMilisec = 0;
        let waitSeconds = "00";
        let waitMinutes = "00";
        if (props.longestWait) {
            longgestWaitMilisec = Math.abs(new Date() - new Date(props.longestWait));
            waitSeconds = Math.floor(longgestWaitMilisec / 1000);
            waitMinutes = Math.floor(waitSeconds / 60);
            if (waitMinutes > 0) {
                if (waitMinutes < 10) {
                    waitMinutes = "0" + waitMinutes.toString();
                }
                waitSeconds = waitSeconds % 60;
            }
            else {
                waitMinutes = "00"
            }
            if (waitSeconds < 10) {
                waitSeconds = "0" + waitSeconds.toString();
            }
        }
        setClock(waitMinutes + ":" + waitSeconds);
    }
    return (
        <td>{clock}</td>
    );
}
export default TimerClock;