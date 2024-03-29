
<template>
  <a-layout class="layout">

    <a-layout-header>
      <div class="logo" />
      <a-menu theme="dark" mode="horizontal" :style="{ lineHeight: '64px' }">
        <a-menu-item key="1">
          <router-link to='/'>{{ $t('Home') }}</router-link>
        </a-menu-item>
        <a-menu-item key="2">
          <router-link :to='`/topics/${currentTopicName}/graph`'>{{ $t('Graph') }}</router-link>
        </a-menu-item>
        <a-menu-item key="3">
          <router-link :to='`/topics/${currentTopicName}/characters`'>{{ $t('Characters') }}</router-link>
        </a-menu-item>
        <a-menu-item key="4">
          <router-link :to='`/topics/${currentTopicName}/mainlines`'>{{ $t('Mainlines') }}</router-link>
        </a-menu-item>
        <a-menu-item key="5">
          <router-link :to='`/topics/${currentTopicName}/groups`'>{{ $t('Groups') }}</router-link>
        </a-menu-item>
        <a-menu-item key="6">
          <router-link :to='`/topics/${currentTopicName}/paths`'>{{ $t('Paths') }}</router-link>
        </a-menu-item>
        <a-menu-item key="7">
          <router-link to='/topics/edit'>{{ $t('Topics') }}</router-link>
        </a-menu-item>
        <a-menu-item key="8">
          <router-link :to='`/topics/${currentTopicName}/edit/addcharacter`'>{{ $t('Edit') }}</router-link>
        </a-menu-item>

        <!-- TODO: float:right does not work-->
        <a-menu-item key="9" :disabled="true" style="float:rigt">
          <a-select v-model:value="currentTopicName" show-search placeholder="Select topic" style="width: 200px"
            :options="selectTopicOptions" @change="handleChangeTopic">
          </a-select>
        </a-menu-item>

        <!-- TODO: support i18n -->
        <a-menu-item key="10" :disabled="true" style="float:rigt">
          <a-select v-model:value="$i18n.locale" style="width: 100px"
            :options="selectLanguageOptions">
          </a-select>
        </a-menu-item>
      </a-menu>
    </a-layout-header>

    <a-layout-content style="padding: 0 50px">
      <router-view></router-view>
    </a-layout-content>

    <a-layout-footer style="text-align: center">
      <div>
        <a href="https://github.com/topicland/TopicLand" target="_blank">TopicLand</a> © 2022-2023 <a href="https://beian.miit.gov.cn/" target="_blank">{{$t('ICP_MESSAGE')}}</a>
      </div>
    </a-layout-footer>
  </a-layout>

</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted, watch } from 'vue'
import axios from 'axios'
import { SelectTypes } from 'ant-design-vue/es/select';
import { useRouter, useRoute } from 'vue-router'

type SelectItem = {
  value: string;
  label: string;
};

export default defineComponent({
  name: "Home",

  setup() {
    const router = useRouter()
    const route = useRoute()

    const currentTopicName = ref<string>("");
    const selectTopicOptions = ref<SelectTypes['options']>([]);

    const selectLanguageOptions = ref<SelectTypes['options']>([
      { "value": "en", "label": "en" },
      { "value": "zh", "label": "zh" }
    ]);

    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };


    watch(
      () => route.params.topic,
      async newTopicName => {
        // Update the selected topic name when router has been changed
        if (newTopicName) {
          currentTopicName.value = newTopicName;
        }
      }
    )

    const handleChangeTopic = (value: string) => {
      // Watch router and jump to new path with new topic name
      const currentPath = route.fullPath;
      if (currentPath.startsWith("/topics/") && currentPath != "/topics/edit") {
        // Split the path and replace the topic name in the path
        const pathSplitedList = currentPath.split("/");
        // Only update when the path has been changed
        if (pathSplitedList[2] != currentTopicName.value) {
          pathSplitedList[2] = currentTopicName.value;
          const pathWithNewTopic = pathSplitedList.join("/");
          router.replace({ path: pathWithNewTopic });
        }
      }
    }

    const initTopicOptions = () => {
      axios.get(`/api/topics/names`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.topics.forEach(theTopic => {
            selectItems.push({ "value": theTopic, "label": theTopic })
          });
          selectTopicOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTopicOptions();
    })

    return {
      selectTopicOptions,
      currentTopicName,
      filterOption,
      handleChangeTopic,

      selectLanguageOptions
    };
  }

});

</script>
