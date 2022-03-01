import { useEffect, useRef } from "react";
import ReactDOM from 'react-dom'

const NewWindow = ({ children, onClose, name }) => {
    let externalWindowRef = useRef(null);
    const containerElRef = useRef(document.createElement('div'));
    useEffect(() => {
        if (!externalWindowRef.current) {
            externalWindowRef.current = window.open('', name);
            externalWindowRef.current.document.body.appendChild(containerElRef.current);
            externalWindowRef.current.onunload = () => onClose();
            console.log('new-window')
        }
    }, [name])
    return (
        ReactDOM.createPortal(children, containerElRef.current)
    );
};

export default NewWindow;