<script lang="ts" setup>
// Columns
const columns = [{
  key: 'id',
  label: '#',
  sortable: true
}, {
  key: 'serial_num',
  label: 'serial_num',
  sortable: true
}, {
  key: 'note',
  label: 'note',
  sortable: true
},
{key: 'actions'}
]

const selectedColumns = ref(columns)
const columnsTable = computed(() => columns.filter((column) => selectedColumns.value.includes(column)))

// Selected Rows
const selectedRows = ref([])


// Actions

const search = ref('')
const selectedStatus = ref([])
const searchStatus = computed(() => {
  if (selectedStatus.value?.length === 0) {
    return ''
  }

  if (selectedStatus?.value?.length > 1) {
    return `?completed=${selectedStatus.value[0].value}&completed=${selectedStatus.value[1].value}`
  }

  return `?completed=${selectedStatus.value[0].value}`
})

const resetFilters = () => {
  search.value = ''
  selectedStatus.value = []
}

// Pagination
const page = ref(1)
const pageCount = ref(5)

const pageTotal = (await useAsyncData(()=> $fetch('http://127.0.0.1:8000/api/equipment/'))).data.value.count

const pageFrom = computed(() => (page.value - 1) * pageCount.value + 1)
const pageTo = computed(() => Math.min(page.value * pageCount.value, pageTotal))

// Data
const { data: todos, pending } = await useLazyAsyncData('todos', () => $fetch<{
  id: number
  serial_num: string
  note: string
}[]>(`http://localhost:8000/api/equipment/${searchStatus.value}`, {
  query: {
    search: search.value,
    'offset': pageCount.value*(page.value-1)
  }                                         
}), {
  default: () => [],
  watch: [page, search, searchStatus, pageCount]
})


</script>

<template>

  <UCard
    class="w-full"
    :ui="{
      base: '',
      ring: '',
      divide: 'divide-y divide-gray-200 dark:divide-gray-700',
      header: { padding: 'px-4 py-5' },
      body: { padding: '', base: 'divide-y divide-gray-200 dark:divide-gray-700' },
      footer: { padding: 'p-4' }
    }"
  >
    <template #header>
      <h2 class="font-semibold text-xl text-gray-900 dark:text-white leading-tight">
        Equipments
      </h2>
    </template>

    <!-- Filters -->
    <div class="flex items-center justify-between gap-3 px-4 py-3">
      <UInput v-model="search" icon="i-heroicons-magnifying-glass-20-solid" placeholder="Search..." />
    </div>

    <div class="flex justify-between items-center w-full px-4 py-3">


      <div class="flex gap-1.5 items-center">


        <USelectMenu v-model="selectedColumns" :options="columns" multiple>
          <UButton
            icon="i-heroicons-view-columns"
            color="gray"
            size="xs"
          >
            Columns
          </UButton>
        </USelectMenu>

        <UButton
          icon="i-heroicons-funnel"
          color="gray"
          size="xs"
          :disabled="search === '' && selectedStatus.length === 0"
          @click="resetFilters"
        >
          Reset
        </UButton>
      </div>
    </div>

    <!-- Table -->
    <UTable
      :rows=todos.results
      :columns="columnsTable"
      :loading="pending"
      sort-asc-icon="i-heroicons-arrow-up"
      sort-desc-icon="i-heroicons-arrow-down"
      class="w-full"
      :ui="{ td: { base: 'max-w-[0] truncate' } }"
    >

    <template #actions-data="{ row }">
      {{ row.note.value }}
      <NuxtLink :to="`/equipment/${ row.id }`" >
        Edit
  </NuxtLink>
      <!-- </UDropdown> -->
    </template>
      
    </UTable>

    <!-- Number of rows & Pagination -->
    <template #footer>
      <div class="flex flex-wrap justify-between items-center">
        <div>
          <span class="text-sm leading-5">
            Showing
            <span class="font-medium">{{ pageFrom }}</span>
            to
            <span class="font-medium">{{ pageTo }}</span>
            of
            <span class="font-medium">{{ pageTotal }}</span>
            results
          </span>
        </div>

        <UPagination
          v-model="page"
          :page-count="pageCount"
          :total="pageTotal"
          :ui="{
            wrapper: 'flex items-center gap-1',
            rounded: '!rounded-full min-w-[32px] justify-center',
            default: {
              activeButton: {
                variant: 'outline'
              }
            }
          }"
        />
      </div>
    </template>
  </UCard>

    <PostForm/>
</template>