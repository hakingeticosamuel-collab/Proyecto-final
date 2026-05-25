import { createApp } from 'vue'
import App from './App.vue'
import './assets/tailwind.css'

const app = createApp(App)

// mark app mounted so overlay knows initialization succeeded
app.mixin({
	mounted() {
		try{ window.__APP_MOUNTED__ = true }catch(e){}
	}
})

app.mount('#app')
