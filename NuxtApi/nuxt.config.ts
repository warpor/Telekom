// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devServer: {
    host: '0' 
  },
  ssr: false,
  devtools: { enabled: true },
  modules: ['@nuxt/ui']
})

