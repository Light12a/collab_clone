import React, { Suspense } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import store from './redux/store';
import { Provider } from 'react-redux';
import * as serviceWorker from './service/serviceWorker';
// import 'antd/dist/antd.css';
import './i18next/i18next'
ReactDOM.render(

  <React.StrictMode>
    <Provider store={store}>
      <Suspense fallback={(<div>Loading</div>)}>
        <App />
      </Suspense>
    </Provider>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
