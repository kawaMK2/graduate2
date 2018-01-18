
<script>
  import { Bar } from 'vue-chartjs'

  export default {
    extends: Bar,
    props: ['data', 'options'],
    mounted () {
      // 下記データでグラフをレンダリング
      this.renderChart({
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: this.data,
        options: this.options
      })
    }
  }
</script>

<style scoped>

</style>
