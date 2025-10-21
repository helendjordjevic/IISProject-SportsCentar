import { createApp, h } from 'vue';
import { createStore } from "vuex";
import createPersistedState from 'vuex-persistedstate';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

//bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
//icons - fontawesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faMagnifyingGlass, faUserSecret, faHeart as faSolidHeart,faTrashCan,faSort} from '@fortawesome/free-solid-svg-icons';
import {faComment, faHeart, faUser,faPaperPlane,faPenToSquare} from '@fortawesome/free-regular-svg-icons';

// Create Vuex store
const store = createStore({
    state: {
        isLoggedIn: !!localStorage.getItem('token'),
        user: {
            username: null,
            name: null,
            surname: null,
            roles: null
        }
    },
    mutations: {
        setUser(state, user) {
            state.user = {
                username: user.username,
                name: user.name,
                surname: user.surname,
                roles: user.roles
            };
        },
        async login(state, token) {
            state.isLoggedIn = true;
            const decodedToken = jwtDecode(token);
            try {
                const response = await axios.get(`http://localhost:8081/user/${decodedToken.sub}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.commit('setUser', response.data);
                // console.log("User details fetched:", response.data);
            } catch (error) {
                console.error("Error fetching user details:", error);
            }
        },
        logout(state) {
            state.isLoggedIn = false;
            state.user = {
                username: null,
                name: null,
                surname: null,
                roles: null
            };
        }
    },
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })]
});

// Add Axios interceptor
axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

/* add icons to the library */
library.add(faUserSecret,faMagnifyingGlass, faUser, faHeart, faComment, faPaperPlane, faSolidHeart,faTrashCan,faPenToSquare,faSort);

createApp(App).use(router).use(store).component('font-awesome-icon', FontAwesomeIcon).mount('#app')
export { store }; // Export the store to be used in index.js