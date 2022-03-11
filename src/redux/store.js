import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './reducers/index';

const loggerMDW = store => next => action => {
  console.log('dispatch', action)
  let result = next(action)
  console.log('next state', store.getState())
  console.dir(result)
  if (result.type.includes('rejected') && !result.type.includes('login')) {
    if (result.payload?.response?.status === 401 || !result.payload?.response) {
      next({ type: 'LOGOUT' })
    }
  }
  return result
}

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMDW) => getDefaultMDW().concat(loggerMDW)
});

export default store;