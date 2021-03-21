<template>
  <div class="hello">
    <b-alert variant="danger" :show="showAlert">Please upload .wav file!</b-alert>
    <h1>{{ msg }}</h1>
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" accept=".wav" @change="handleFileUpload($event)"/>
      </label>
    </div>
    <div>
      <b-button v-on:click="submitFile()">Submit</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios, { AxiosResponse } from 'axios';

@Component
export default class HelloWorld extends Vue {
  @Prop() private msg!: string;
  //initalize empty file
  file: File = new File([""], "");
  apiResponse = "";
  showAlert = false;

  handleFileUpload(event: Event): void{
    const target = event.target as HTMLInputElement
    let file: File;
    file = target.files[0];
    // check if file is .wav
    if (file['type'] === 'audio/wav'){
      this.file = file;
    } else {
      this.showAlert  = true;
      setTimeout(() => {this.showAlert = false}, 3000);
    }
  }

  async submitFile(): Promise<void>{
    let formData: FormData = new FormData();
    formData.append('file', this.file);
    const response = await axios.post(`http://localhost:5000/file`, formData).then((response) => {
      console.log(response);
    })
  }

  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
