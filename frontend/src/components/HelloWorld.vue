<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height">
      <div class="text-center">
        <v-btn prepend-icon="mdi-check-circle">
          <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>

          Import Excel
        </v-btn>

        <v-btn prepend-icon="mdi-check-circle">
          <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>

          Export Excel
        </v-btn>
      </div>

      <v-data-table :headers="headers" :items="currentParts">
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title
              >Master Parts changeover matrix </v-toolbar-title
            >
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ props }">
                <v-btn color="primary" dark class="mb-2" v-bind="props">
                  New Part
                </v-btn>
              </template>
              <v-card>
                <v-card-title>
                  <span class="text-h5">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text v-if="this.editedIndex === -1">
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="newParts"
                          label="Current"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-text v-else>
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.current"
                          label="Current"
                        ></v-text-field>
                      </v-col>

                      <v-col
                        v-for="part in parts"
                        :key="part"
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="editedItem[part]"
                          :label="part"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue-darken-1" variant="text" @click="close">
                    Cancel
                  </v-btn>
                  <v-btn color="blue-darken-1" variant="text" @click="save">
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="text-h5"
                  >Are you sure you want to delete this item?</v-card-title
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="blue-darken-1"
                    variant="text"
                    @click="closeDelete"
                    >Cancel</v-btn
                  >
                  <v-btn
                    color="blue-darken-1"
                    variant="text"
                    @click="deleteItemConfirm"
                    >OK</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon size="small" class="me-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon size="small" @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize"> Reset </v-btn>
        </template>
      </v-data-table>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    newParts: "",
    parts: ["A", "B", "C"],
    headers: [],
    currentParts: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
    defaultItem: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0,
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Part" : "Edit Part";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
    parts: {
      handler(newVal, oldVal) {
       this.initialize();
      },
      deep: true, 
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      const newParts = [];

      this.parts.forEach((part) => {
        const partObject = { current: part };
        this.parts.forEach((p) => {
          partObject[p] = 0;
        });
        newParts.push(partObject);
      });

      this.currentParts = newParts;

      this.headers = [
        {
          title: "",
          align: "start",
          sortable: false,
          key: "current",
        },
        ...this.parts.map((part) => {
          return {
            title: part,
            key: part,
          };
        }),
        {
          title: "Edit Part",
          key: "actions",
        },
      ];
    },

    editItem(item) {
      this.editedIndex = this.currentParts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.currentParts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.currentParts.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.currentParts[this.editedIndex], this.editedItem);
      } else {
        this.parts.push(this.newParts);
      }
      this.close();
    },
  },
};
</script>
