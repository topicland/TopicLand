
<template>

  <div style="background-color: #ececec; padding: 20px">

    <div v-for="groupCharactersItem in groupCharactersData">

      <br/>

      <h2><router-link :to='`/topics/${topic}/groups/${groupCharactersItem.group_name}`'>{{ groupCharactersItem.group_name }}</router-link></h2>

      <a-row :gutter="16">
        <div v-for="character in groupCharactersItem.characters" >
          <a-col :span="4">
            <a-card hoverable style="width: 240px" @click="redirectToCharacterPage(character.name)">
              <template #cover>
                  
              </template>
              <a-card-meta :title="character.name">
                <template #description>{{ character.note }}</template>
              </a-card-meta>
            </a-card>
          </a-col>
        </div>
      </a-row>

    </div>

  </div>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

interface CharacterData {
  name: string,
  note: string,
}

interface GroupCharactersData {
  group_name: string,
  characters: CharacterData[]
}

export default defineComponent({
  name: "GroupsList",
  props: {
    topic: String,
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const router = useRouter()

    const groupCharactersData = ref<GroupCharactersData>();

    const redirectToCharacterPage = (character_name) => {
      router.push({ path: `/topics/${props.topic}/characters/${character_name}` })
    }

    watch(() => props.topic, (first, second) => {
      init();
    });

    const init = () => {
        axios.get(`/api/topics/${props.topic}/groups_characters`)
        .then(response => {
          groupCharactersData.value = response.data.groups_and_characters;
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      init();
    })

    return {
      API_BASE_URI,

      groupCharactersData,

      redirectToCharacterPage
    }
  }
})
</script>
