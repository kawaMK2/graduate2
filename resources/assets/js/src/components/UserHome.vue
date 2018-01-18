<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex xs4>
        <v-card>
          <v-container fluid grid-list-lg>
            <v-layout row>
              <v-flex>
                <!--<v-card-media height="60px" contain>-->
                  <v-avatar style="background-color: rgba(0,0,0,0.2)" class="elevation-5">
                    <img v-if="user.thumbnail !== null" v-bind:src="user.thumbnail"/>
                    <v-icon v-else>account_circle</v-icon>
                  </v-avatar>
                <!--</v-card-media>-->
              </v-flex>
              <v-flex>
                <div>
                  <div class="headline">{{ getFullName }}</div>
                  <div>{{ getCurrentGrade }}</div>
                </div>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card>
      </v-flex>

      <v-flex xs8>
        <v-layout column>
          <v-flex>
            <v-card>
              <time-chart :data="chartData" :height="150"/>
            </v-card>
          </v-flex>
          <v-flex>
            <v-data-table
              v-bind:headers="headers"
              :items="notes"
              hide-actions
              disable-initial-sort
              class="elevation-1"
            >
              <template slot="items" slot-scope="props">
                <td>{{ props.item.date }}</td>
                <td class="text-xs-center">
                  <router-link :to="{ name: 'note', params: { noteId: props.item.id }}">
                    {{ props.item.title }}
                  </router-link>
                </td>
                <td class="text-xs-center">{{ props.item.start }}</td>
                <td class="text-xs-center">{{ props.item.end }}</td>
                <td class="text-xs-center">{{ props.item.elapsed_time }}</td>
                <td class="text-xs-center">{{ props.item.locate }}</td>
              </template>
            </v-data-table>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'
  import TimeChart from './TimeChart'

  export default {
    name: 'user-home',
    data () {
      return {
        user: {},
        notes: [],
        headers: [
          {text: 'Notes', align: 'left', sortable: false, value: 'date'},
          {text: 'Title', align: 'center', sortable: false, value: 'title'},
          {text: 'Start time', align: 'center', sortable: false, value: 'start'},
          {text: 'End time', align: 'center', sortable: false, value: 'end'},
          {text: 'Elapsed time', align: 'center', sortable: false, value: 'elapsed_time'},
          {text: 'Location', align: 'center', sortable: false, value: 'locate'}
        ],
        datacollection: {
          labels: ['January', 'February'],
          datasets: [
            {
              label: 'Data One',
              backgroundColor: '#f87979',
              data: [40, 20]
            }
          ]
        },
        chartData: [
          {
            label: '研究時間',
            backgroundColor: '#f87979',
            data: [4, 20, 12, 9, 10, 4, 9, 20, 4, 20, 12, 11]
          }
        ]
      }
    },
    beforeMount: function () {
      console.log('mounted')
      axios.get('/api/user/' + this.$route.params.username + '/')
        .then((response) => {
          this.user = response.data
        })
        .catch((error) => {
          console.log(error)
        })
      axios.get('/api/notes/' + this.$route.params.username + '/')
        .then((response) => {
          this.notes = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },
    mounted () {
      this.renderChart(this.datacollection, {responsive: true, maintainAspectRatio: false})
    },
    computed: {
      getFullName: function () {
        return this.user.last_name + ' ' + this.user.first_name
      },
      getCurrentGrade: function () {
        let belongs = this.user.belongs
        if (belongs.length > 1) belongs.sort((a, b) => a.priority - b.priority)
        return belongs[0].formal_name
      }
    },
    components: {
      TimeChart
    }
  }
</script>

<style scoped>

</style>
