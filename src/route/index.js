import  React from 'react';
import { useSelector } from 'react-redux';
import Keypad from '../features/keypad/Keypad';
import WaitingList from '../features/watingList/WaitingList';
import SettingScreen from '../features/settingScreen/SettingScreen'
import HomePage from '../features/homepage/HomePage';
import IncomingMemo from '../features/talkcript/IncomingMemo';

const Route = () => {
    const { currentRoute } = useSelector(state => state.route)
    const ConponentName = routeDefine[currentRoute]
    return <ConponentName />
}
const DefaultCoponent = () => {
    return <h1> nothing here</h1>
}
const routeDefine = {
    main: HomePage,
    present: DefaultCoponent,
    waiting: WaitingList,
    memo: DefaultCoponent,
    setting: SettingScreen,
    incoming: IncomingMemo
}


export default React.memo(Route);