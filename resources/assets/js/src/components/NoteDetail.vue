<template>
  <v-container fluid grid-list-md>
    <!--{{ note }}-->
    <quill-editor :content="note.content"/>
  </v-container>
</template>

<script>
  import axios from 'axios'
  import 'quill/dist/quill.core.css'
  import 'quill/dist/quill.snow.css'
  import 'quill/dist/quill.bubble.css'

  import { quillEditor } from 'vue-quill-editor'

  export default {
    name: 'note-detail',
    data () {
      return {
        note: {},
        content: '本日は晴天なり'
      }
    },
    beforeMount: function () {
      console.log('mounted')
      axios.get('/api/note/' + this.$route.params.noteId + '/')
        .then((response) => {
          this.note = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
    components: {
      quillEditor
    }
  }
</script>

<style scoped>

</style>
