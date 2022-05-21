import { defineStore } from "pinia";

const useStore = defineStore({
  id: "store",
  state: () => {
    return {
      server: "http://localhost:8000/api/v1",      
      current_matches: null,
      match: null,
      user: null
    }
  },
  getters: {        
  },
  actions: {
    async refreshTokens() {
      const credentials = JSON.parse(localStorage.getItem('credentials') || '{}');
      const refresh_token = credentials?.refresh_token
      const url = `${this.server}/refresh/`;
      console.log(credentials)
      const options = {
        method: "POST",
        headers: new Headers({"Content-Type": "application/json"}),
        body: JSON.stringify({"refresh": refresh_token}),
        redirect: 'follow'
      }
      console.log(options, url);
      const resp = await fetch(url, options);
      const data = await resp.json();      
      if (!resp.ok) {
        localStorage.setItem("login", JSON.stringify({'state': "login_required"}))
        return resp
      }
      // credentials.access_token = data.access_token;
      // credentials.refresh_token = data.refresh_token;
      // localStorage.setItem("credentials", JSON.stringify(credentials))
      return resp
    },
    async request(url, options)  {
      const resp = await fetch(url, options);
      const data = await resp.json();

      if (!resp.ok) {
        if (data.code == 'token_not_valid') {
          let refrsh_resp = await this.refreshTokens();
          console.log(url, refrsh_resp);
          if (refrsh_resp.ok && data.code != 'token_not_valid') {
            this.getCurrentMatches(url, options);            
          }          
        }
      }

      console.log(data);
      return data;
    },
    async securedRequest(url, method) {
      const access_token = JSON.parse(localStorage.getItem("credentials") || '{}')?.access_token;
      const options = {
        method: method,
        headers: new Headers({"Authorization": `Bearer ${access_token}`})
      };            
      const data = await this.request(url, options);      
      return data
    },
    async getCurrentMatches() {
      const url = `${this.server}/current-matches/`;
      const data = await this.securedRequest(url, "GET");
      this.current_matches = data.data;      
      return data;
    },
    async getMatchDetail(match_id) {
      const url = `${this.server}/match/${match_id}/`;
      const data = await this.securedRequest(url, "GET");
      this.match = data.data;      
      console.log(data)
      return data;
    },
    async getUserDetails() {
      const url = `${this.server}/user-details/`;
      const data = await this.securedRequest(url, "GET");
      this.user = data.data;      
      console.log(data)
      return data;
    } 
  },
});

export default useStore;