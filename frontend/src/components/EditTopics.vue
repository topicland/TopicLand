
<template>

  <div style="padding: 20px">
    <h1> Manage Topics</h1>

    <!-- Form to create topic -->
    <a-form layout="inline" :model="formState" @finish="handleCreateTopicFinish" @finishFailed="handleFinishFailed">
      <a-form-item>
        <a-input v-model:value="formState.name" placeholder="Topic name">
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          Create Topic
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to delete topic -->
    <a-form layout="inline" :model="deleteTopicFormState" @finish="handleDeleteTopicFinish"
      @finishFailed="handleFinishFailed">
      <a-form-item>
        <a-select v-model:value="deleteTopicFormState.name" show-search placeholder="Select topic" style="width: 200px"
          :options="selectTopicOptions" >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          Delete Topic
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to export topic -->
    <a-form layout="inline" :model="exportTopicFormState" @finish="handleExportTopic" >
      <a-form-item>
        <a-select v-model:value="exportTopicFormState.topic" show-search placeholder="Select topic" style="width: 200px"
          :options="selectTopicOptions" >
        </a-select>
      </a-form-item>
      <a-form-item>
        <a-input v-model:value="exportTopicFormState.path" placeholder="Export directory"></a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          Export Topic
        </a-button>
      </a-form-item>
    </a-form>

    <br />
    <!-- Form to import topic -->
    <a-form layout="inline" :model="importTopicFormState" @finish="handleImportTopic" >
      <a-form-item>
        <a-input v-model:value="importTopicFormState.topic" placeholder="Topic name"></a-input>
      </a-form-item>
      <a-form-item>
        <a-input v-model:value="importTopicFormState.path" placeholder="Import directory"></a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" html-type="submit">
          Import Topic
        </a-button>
      </a-form-item>
    </a-form>


    <br /><br />
    <!-- List of all topics -->
    <h1> Topics List</h1>
    <a-list item-layout="horizontal" :data-source="topics">
      <template #renderItem="{ item }">
        <a-list-item>
          <router-link :to='`/topics/${item}/graph`'>{{ item }}</router-link>
        </a-list-item>
      </template>
    </a-list>

  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import type { UnwrapRef } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import type { FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import { SelectTypes } from 'ant-design-vue/es/select';
import GraphDetail from './GraphDetail.vue';
import { string } from 'vue-types';

type SelectItem = {
  value: string;
  label: string;
};

interface FormState {
  name: string;
}

interface ImportExportTopicFormState {
  name: string,
  path: string
}

export default defineComponent({
  name: "EditTopics",
  props: {},
  components: {
    GraphDetail
  },
  setup() {

    const topics = ref([]);
    const chosenTopicName = ref("");

    // Select options for selecting topic
    const selectTopicOptions = ref<SelectTypes['options']>([]);
    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const formState: UnwrapRef<FormState> = reactive({
      name: ''
    });

    const deleteTopicFormState: UnwrapRef<FormState> = reactive({
      name: ''
    });

    const exportTopicFormState: UnwrapRef<ImportExportTopicFormState> = reactive({
      topic: '',
      path: '',
    });

    const importTopicFormState: UnwrapRef<ImportExportTopicFormState> = reactive({
      topic: '',
      path: '',
    });

    const handleCreateTopicFinish: FormProps['onFinish'] = values => {

      axios.post(`/api/topics`, {
        "name": formState.name
      })
        .then(response => {
          message.success('Success to create topic: ' + formState.name);
          
          initTopicListData()
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleDeleteTopicFinish: FormProps['onFinish'] = values => {
      axios.delete(`/api/topics/${deleteTopicFormState.name}`)
        .then(response => {
          message.success('Success to delete topic: ' + deleteTopicFormState.name);
          initTopicListData();
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleExportTopic: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${exportTopicFormState.topic}/export`, {
        path: exportTopicFormState.path
      })
      .then(response => {
        message.success('Success to export topic: ' + exportTopicFormState.topic);
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };

    const handleImportTopic: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${importTopicFormState.topic}/import`, {
        path: importTopicFormState.path
      })
      .then(response => {
        message.success('Success to import topic: ' + importTopicFormState.topic);
        initTopicListData();
      })
      .catch(error => {
        console.log(error);
      });
    };

    const handleFinishFailed: FormProps['onFinishFailed'] = errors => {
      console.log(errors);
    };

    const previewGraph = (name) => {
      chosenTopicName.value = name;
    }

    const getRandomInt = (min, max) => {
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    const initTopicListData = () => {
      axios.get(`/api/topics`)
        .then(response => {
          topics.value = response.data.topics;

          // Set select options
          const selectItems: SelectItem[] = [];
          response.data.topics.forEach(theTopic => {
            selectItems.push({ "value": theTopic, "label": theTopic })
          });
          selectTopicOptions.value = [...selectItems];

          // Select the random topic to display by default
          const randomIndex = getRandomInt(0, response.data.topics.length - 1);
          chosenTopicName.value = response.data.topics[randomIndex];
        })
        .catch(error => {
          console.log(error);
        });
    }

    onMounted(() => {
      initTopicListData();
    })

    return {
      topics,
      chosenTopicName,
      formState,
      handleCreateTopicFinish,

      deleteTopicFormState,
      handleDeleteTopicFinish,
      handleFinishFailed,
      previewGraph,

      selectTopicOptions,
      filterOption,

      exportTopicFormState,
      importTopicFormState,
      handleExportTopic,
      handleImportTopic
    }
  }
})
</script>