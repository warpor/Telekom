<script setup lang="ts">
const route = useRoute()

defineProps(['modelValue'])

import { ref } from 'vue'
import type { FormError, FormSubmitEvent } from '@nuxt/ui/dist/runtime/types'

const equipment_type = (await useAsyncData(()=> $fetch('http://127.0.0.1:8000/api/equipment-type/'))).data.value.results  
const equipment_type_names = equipment_type.map(a => a.type_name) 

let id_url =`http://127.0.0.1:8000/api/equipment/${route.params.id}/`
let equipment_info: any = (await useAsyncData(()=> $fetch(id_url))).data.value

const type_name = equipment_type_names[equipment_info.type_id-1]


const state = ({
  id: route.params.id,
  type_id: type_name,
  serial_num: equipment_info.serial_num,
  note: equipment_info.note
})

const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.type_id) errors.push({ path: 'Types', message: 'Необходимо выбрать тип устройства' })
  if (!state.serial_num) errors.push({ path: 'SerialNum', message: 'Необходим серийный номер' })
  if (!state.note) errors.push({ path: 'Note', message: 'Необходимо ввести примечание' })
  return errors
}

function get_form_for_sending(forms)
{
  let form = forms
  form.type_id = (equipment_type.find((obj) => {return obj.type_name === forms.type_id;}).id)
  return form
}

function change() {
formRequest().then( (result) => {
    post()
}).catch( (error) => {
    alert(error.data.non_field_errors)
});
}

async function post() {
  alert("Запись успешно изменена")
  await navigateTo("/equipment") 
}

async function formRequest() {

  let form = get_form_for_sending(state)

  return await $fetch(id_url, { 
    headers: {

        "Content-Type": "application/json"
    },
    method: 'PUT',
    body: form
} );
}

async function delete_form() {

  let result = confirm("Хотите удалить запись?")
  if (result == true)
    {await $fetch(id_url, { 
      method: 'DELETE',
  } );
  alert("Запись успешно удалена")
  await navigateTo("/equipment")
}

}

async function back()
{
  await navigateTo("/equipment")
}




</script>

<template>
  <UForm
    :value="modelValue"
    :validate="validate"
    :state="state"
    @submit="change"
  >
   <UFormGroup label="Тип оборудования" name="Types">
      <USelect v-model="state.type_id" :options="equipment_type_names"/>
    </UFormGroup>


    <UFormGroup label="Серийный номер" name="SerialNum">
      <UInput v-model="state.serial_num" />
    </UFormGroup>

    <UFormGroup label="Примечание" name="Note">
      <UInput v-model="state.note"/>
    </UFormGroup>

    <UButton type="change">
        Сохранить
    </UButton>

      </UForm>
    
    <UButton type="delete" @click="delete_form">
        Удалить
    </UButton>

      <br>
        
    <UButton type="delete" @click="back">
        Назад
    </UButton>




</template>
 

  