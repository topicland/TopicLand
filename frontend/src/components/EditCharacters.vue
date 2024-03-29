
<template>

  <h1>{{ $t('CreateCharacter') }}</h1>
  <a-form layout="inline" :model="formState" @finish="handleSubmitForm" @finishFailed="handleSubmitFormFailed">
    <a-form-item :label="$t('Name')" name="name" :rules="[{ required: true, message: 'Please input name!' }]">
      <a-input v-model:value="formState.name" />
    </a-form-item>

    <a-form-item :label="$t('Note')" name="note">
      <a-input v-model:value="formState.note" />
    </a-form-item>

    <a-form-item>
      <a-upload v-model:fileList="uploadImageFileList" :action="`${API_BASE_URI}/api/topics/${topic}/character_image`"
        list-type="picture" :multiple="false">
        <a-button>
          <upload-outlined></upload-outlined>
          {{ $t('UploadImage') }}
        </a-button>
      </a-upload>
    </a-form-item>

    <a-form-item>
      <a-button type="primary" html-type="submit" :disabled="formState.name === ''">
        {{ $t('Submit') }}
      </a-button>
    </a-form-item>
  </a-form>

  <br /><br />
  <h1>{{ $t('RenameCharacter') }}</h1>
  <a-form layout="inline" :model="renameFormState" @finish="handleSubmitRenameForm" @finishFailed="handleSubmitFormFailed">

    <a-form-item>
      <span>{{ $t('CharacterName') }}: &nbsp;</span>
      <a-select v-model:value="renameFormState.character_name" show-search style="width: 200px"
        :options="selectCharacterOptions" :filter-option="filterOption"></a-select>
    </a-form-item>

    <a-form-item :label="$t('NewName')" :rules="[{ required: true, message: 'Please input target name!' }]">
      <a-input v-model:value="renameFormState.new_name" />
    </a-form-item>

    <a-form-item>
      <a-button type="primary" html-type="submit"
        :disabled="renameFormState.character_name === '' && renameFormState.new_name === ''">
        {{ $t('Submit') }}
      </a-button>
    </a-form-item>
  </a-form>

  <br /><br />
  <h1>{{ $t('UpdateCharactersWeights') }}</h1>
  <a-select v-model:value="updateWeightsAlgorithm" :placeholder="$t('Algorithm')" style="width: 300px"
    :options=updateWeightsAlgorithmOptions></a-select>
  <a-button type="primary" @click="updateCharactersWeights">
    {{ $t('Submit') }}
  </a-button>

  <br /><br /><br />
  <h1>{{ $t('UpdateCharactersWeights') }}</h1>
  <a-button type="primary" @click="clearUnusedImages">
    {{ $t('ClearUnusedImages') }}
  </a-button>

  <br /><br /><br />
  <h1>{{ $t('CharactersTable') }}</h1>
  <vxe-grid ref="vxeTable" v-bind="vxeTableOptions" v-on="vxeTableHandler">
    <template #name_edit="{ row }">
      <vxe-input v-model="row.name"></vxe-input>
    </template>
    <template #note_edit="{ row }">
      <vxe-textarea v-model="row.note" :autosize="{ minRows: 1, maxRows: 8 }"></vxe-textarea>
    </template>
    <template #weight_edit="{ row }">
      <vxe-input v-model="row.weight"></vxe-input>
    </template>

    <template #operate="{ row }" slot-scope="scope">
      <!-- TODO: icon is not displayed -->
      <vxe-button @click="removeRow(row)" circle status="warning" icon="fa fa-trash-o"></vxe-button>
    </template>
  </vxe-grid>

</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, reactive, ref, onMounted } from 'vue'
import type { UnwrapRef } from 'vue';
import { message } from 'ant-design-vue';
import { VXETable, VxeGridInstance, VxeGridListeners, VxeGridProps } from 'vxe-table'
import type { SelectProps, FormProps, UploadProps } from 'ant-design-vue';
import { UploadOutlined } from '@ant-design/icons-vue';

type SelectItem = {
  value: string;
  label: string;
};

interface FormState {
  name: string;
  note: string;
}

interface RenameFormState {
  character_name: string;
  new_name: string;
}

export default defineComponent({
  name: "EditCharacters",
  components: {
    UploadOutlined
  },
  props: {
    topic: String,
  },
  setup(props) {
    const API_BASE_URI = axios.defaults.baseURL;

    const vxeTable = ref<VxeGridInstance>()
    const vxeTableOptions = reactive<VxeGridProps>({
      border: true,
      keepSource: true,
      id: 'characters_table',
      exportConfig: {},
      importConfig: {},
      columnConfig: {
        resizable: true
      },
      customConfig: {
        storage: true
      },
      editConfig: {
        trigger: 'click',
        mode: 'row',
        showStatus: true
      },
      columns: [
        { field: 'name', title: 'Name', editRender: {}, slots: { edit: 'name_edit' } },
        { field: 'note', title: 'Note', editRender: {}, slots: { edit: 'note_edit' } },
        { field: 'weight', title: 'Weight', slots: { edit: 'weight_edit' } },
        { title: 'Delete', width: 200, slots: { default: 'operate' } }
      ],
      toolbarConfig: {
        buttons: [
          { code: 'insertButton', name: 'New', status: 'primary' },
          { code: 'saveButton', name: 'Save', status: 'success' }
        ],
        import: false, // TODO: Support and test
        export: true,
        zoom: true,
        custom: true,
        refresh: false
      },
      data: []
    })

    const vxeTableHandler: VxeGridListeners = {
      toolbarButtonClick({ code }) {
        const $grid = vxeTable.value
        switch (code) {
          case 'insertButton': {
            $grid.insert({
            })
            break
          }
          case 'saveButton': {
            const { insertRecords, removeRecords, updateRecords } = $grid.getRecordset()
            VXETable.modal.message({ content: `Add ${insertRecords.length} rows, update ${updateRecords.length} rows, delete ${removeRecords.length} rows`, status: 'success' })

            axios.post(`/api/topics/${props.topic}/characters`, {
              insert_characters: insertRecords,
              update_characters: updateRecords,
              delete_characters: removeRecords
            })
              .then(function (response) {
                console.log(response);
              })
              .catch(function (error) {
                console.log(error);
              });
            break
          }
        }
      }
    }

    const removeRow = async (row: any) => {
      const type = await VXETable.modal.confirm("Are you sure to delete?")
      const $grid = vxeTable.value
      if ($grid) {
        if (type === 'confirm') {
          await $grid.remove(row)
        }
      }
    }


    const uploadImageFileList = ref<UploadProps['fileList']>([]);

    const formState: UnwrapRef<FormState> = reactive({
      name: '',
      note: '',
    });


    const handleSubmitForm: FormProps['onFinish'] = values => {
      axios.post(`/api/topics/${props.topic}/characters`, {
        "name": formState.name,
        "note": formState.note,
      })
        .then(response => {
          message.success(`Success to add character: ${formState.name}`);
          initTableData();
        })
        .catch(error => {
          console.log(error);
        });
    };

    const handleSubmitFormFailed: FormProps['onFinishFailed'] = errors => {
      console.log("Fail to submit form: " + errors);
    };


    const filterOption = (input: string, option: any) => {
      return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
    };

    const selectCharacterOptions = ref<SelectProps['options']>([]);

    const renameFormState: UnwrapRef<RenameFormState> = reactive({
      character_name: '',
      new_name: '',
    });

    const handleSubmitRenameForm: FormProps['onFinish'] = values => {

      axios.put(`/api/topics/${props.topic}/characters/${renameFormState.character_name}/name`, {
        new_name: renameFormState.new_name
      })
      .then(function (response) {
        message.success('Success to rename character name');
        initTableData();
      })
      .catch(function (error) {
        message.error('Fail to rename character names, ' + error);
      });
    };

    const initTableData = () => {
      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          vxeTableOptions.data = response.data.characters;
        })
        .catch(error => {
          console.log(error);
        });
    }

    const updateWeightsAlgorithm = ref(undefined);
    const updateWeightsAlgorithmOptions = ref([
      { value: "PageRank", label: "PageRank" },
      { value: "NondirectedPageRank", label: "PageRank(Nondirected Graph)" }]
    )

    const updateCharactersWeights = () => {
      axios.put(`/api/topics/${props.topic}/weights`, {
        algorithm: updateWeightsAlgorithm.value
      })
        .then(function (response) {
          message.success('Success to update characters weights');
        })
        .catch(function (error) {
          message.error('Fail to update characters weights, ' + error);
        });
      initTableData();
    }

    const clearUnusedImages = () => {
      axios.delete(`/api/topics/${props.topic}/unused_images`)
        .then(response => {
          message.success('Success to clear unused images');
        })
        .catch(error => {
          message.error('Fail to clear unused images');
        });
    }

    onMounted(() => {
      initTableData();

      axios.get(`/api/topics/${props.topic}/characters`)
        .then(response => {
          const selectItems: SelectItem[] = [];
          response.data.characters.forEach(character => {
            selectItems.push({ "value": character.name, "label": character.name })
          });
          selectCharacterOptions.value = [...selectItems];
        })
        .catch(error => {
          console.log(error);
        });
    })

    return {
      API_BASE_URI,

      vxeTable,
      vxeTableOptions,
      vxeTableHandler,
      removeRow,

      uploadImageFileList,
      formState,
      handleSubmitForm,
      handleSubmitFormFailed,

      filterOption,
      selectCharacterOptions,
      renameFormState,
      handleSubmitRenameForm,

      updateCharactersWeights,
      updateWeightsAlgorithm,
      updateWeightsAlgorithmOptions,

      clearUnusedImages
    }
  }
})
</script>
