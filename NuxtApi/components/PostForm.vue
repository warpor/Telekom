<script setup lang="ts">
const route = useRoute()

defineProps(['modelValue'])

import { ref } from 'vue'
import type { FormError, FormSubmitEvent } from '@nuxt/ui/dist/runtime/types'

let equipment_type: any = (await useAsyncData(()=> $fetch('http://127.0.0.1:8000/api/equipment-type/'))).data.value.results  

let equipment_type_ids = equipment_type.map(a => a.id) 


const state = ref({
  type_id: equipment_type_ids[0],
  serial_num: undefined,
  note: undefined
})

const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.serial_num) errors.push({ path: 'SerialNum', message: 'Необходим серийный номер' })
  if (!state.note) errors.push({ path: 'Note', message: 'Необходимо ввести примечание' })
  return errors
}




function submit() {
formRequest().then( (result) => {
    alert("Запись успешно создана")
}).catch( (error) => {
    alert(error.data.non_field_errors)
});
}


async function formRequest() {
  return await $fetch('http://127.0.0.1:8000/api/equipment/', { 
    headers: {

        "Content-Type": "application/json"
    },
    method: 'POST',
    body: state.value
} );
}

</script>

<template>
  <UForm
    :value="modelValue"
    :validate="validate"
    :state="state"
    @submit="submit"
  >
   <UFormGroup label="Тип оборудования" name="Types">
    <USelect v-model="state.type_id" :options="equipment_type_ids"/>
    </UFormGroup>


    <UFormGroup label="Серийный номер" name="SerialNum">
      <UInput v-model="state.serial_num" />
    </UFormGroup>

    <UFormGroup label="Примечание" name="Note">
      <UInput v-model="state.note" type="" />
    </UFormGroup>

    <UButton type="submit">
      Добавить
    </UButton>
  </UForm>
</template>
 