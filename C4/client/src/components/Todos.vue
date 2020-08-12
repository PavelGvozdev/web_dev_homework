<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
      <h2>выполнено {{completedTasks}} задач(и), не выполнено {{tasksNotCompleted}} задач(и)</h2>
      <confirmation :message='message'
                    v-if="showConfirmation"
                    @dismissed='resetConfirmation'
                    >
      </confirmation>
      <b-button-group size="sm">
        <button type="button"
                id="task-add"
                class="btn btn-success d-block"
                v-b-modal.todo-modal>
            Добавить задачу
          </button>
          <button type="button"
                id="save-task"
                class="btn btn-dark d-block"
                @click="saveTodosLocalStorage"
                >
            Сохранить задачи
        </button>
        <button type="button"
                id="load-task"
                class="btn btn-info d-block"
                @click="loadTodosFromLocalStorage"
                >
            Загрузить задачи
        </button>
      </b-button-group>
      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
          <tr>
            <th>Uid</th>
            <th>Описание</th>
            <th>Выполнена?</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(todo, index) in todos" :key="index">
            <td class="todo-uid">{{ todo.uid }}</td>
            <td>{{ todo.description }}</td>
            <td>
              <span v-if="todo.is_completed">Выполнено</span>
              <span v-else>Не выполнено</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button"
                        class="btn btn-secondary btn-sm"
                        v-b-modal.todo-update-modal
                        @click="updateTodo(todo)"
                        >Обновить</button>
                &nbsp;
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="deleteTodo(todo)"
                        >X</button>
              </div>
            </td>
          </tr>
        </tbody>

      </table>

      <b-modal ref="addTodoModal"
            id="todo-modal"
            title="Добавить задачу"
            hide-footer>

        <b-form @submit="onSubmit" @reset="onReset" class="w-100">

          <b-form-group id="form-description-group"
                label="Описание:"
                label-for="form-description-input">

            <b-form-input id="form-description-input"
                    type="text"
                    v-model="addTodoForm.description"
                    required
                    placeholder="Завести задачу">
            </b-form-input>
          </b-form-group>

          <b-form-group id="form-complete-group">
            <b-form-checkbox-group v-model="addTodoForm.is_completed" id="form-checks">
              <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button type="submit" variant="primary">Добавить</b-button>
          <b-button type="reset" variant="danger">Сброс</b-button>
        </b-form>

      </b-modal>

      <b-modal ref="updateTodoModal"
               id="todo-update-modal"
               title="Update"
               hide-footer>
        <b-form @submit="onUpdateSubmit" @reset="onUpdateReset" class="w-100">

          <b-form-group id="form-update-description-group"
                        label="Описание:"
                        label-for="form-update-description-input">
            <b-form-input id="form-update-description-input"
                          type="text"
                          v-model="updateTodoForm.description"
                          required>
            </b-form-input>
          </b-form-group>

        <b-form-group id="form-update-complete-group">
            <b-form-checkbox-group v-model="updateTodoForm.is_completed" id="form-update-checks">
              <b-form-checkbox value="true">Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
        </b-form-group>

          <b-button-group>
              <b-button type="submit" variant="primary">Обновить</b-button>
              <b-button type="reset" variant="danger">Сброс</b-button>
          </b-button-group>

        </b-form>
      </b-modal>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Confirmation from './Confirmation.vue';

const dataURL = 'http://localhost:5000/api/tasks/';

export default {
  name: 'Todo',

  data() {
    return {
      todos: [],

      addTodoForm: {
        description: '',
        is_completed: [],
      },

      updateTodoForm: {
        uid: 0,
        description: '',
        is_completed: [],
      },

      message: '',
      showConfirmation: false,
      completedTasks: 0,
      tasksNotCompleted: 0,

    };
  },

  methods: {
    resetConfirmation() {
      this.showConfirmation = false;
    },

    saveTodosLocalStorage() {
      const serialArr = JSON.stringify(this.todos);
      localStorage.setItem('todosData', serialArr); // сохраняет массив с задачами
      localStorage.setItem('todosNambers', this.todos.length); // сохраняет количество задач
    },

    loadTodosFromLocalStorage() {
      this.todos = JSON.parse(localStorage.getItem('todosData'));
    },

    getTodos() {
      axios.get(dataURL)
        .then((response) => {
          this.todos = response.data.tasks;
          this.completedTasks = 0;
          this.tasksNotCompleted = 0;
          this.todos.forEach((element) => {
            if (element.is_completed) {
              this.completedTasks += 1;
            } else {
              this.tasksNotCompleted += 1;
            }
          });
          // this.saveTodosLocalStorage(this.todos);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = [];
      this.updateTodoForm.description = '';
      this.updateTodoForm.is_completed = [];
    },

    onSubmit(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      let requestData = {};

      requestData = {
        description: this.addTodoForm.description,
        is_completed: this.addTodoForm.is_completed.length > 0,
      };

      axios.post(dataURL, requestData)
        .then(() => {
          this.getTodos();
          this.message = `Задача "${requestData.description}" добавлена`;
          this.showConfirmation = true;
        })
        .catch((error) => {
          console.log(error);
        });
      this.resetForm();
    },

    onReset(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },

    updateTodo(todo) {
      this.updateTodoForm.uid = todo.uid;
      this.updateTodoForm.description = todo.description;
      if (todo.is_completed) {
        this.updateTodoForm.is_completed = [true];
      }
    },

    onUpdateSubmit(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();

      const requestData = {
        description: this.updateTodoForm.description,
        is_completed: this.updateTodoForm.is_completed.length > 0,
      };

      const todoURL = dataURL + this.updateTodoForm.uid;
      axios.put(todoURL, requestData)
        .then(() => {
          this.getTodos();
          this.message = 'Задача обновлена';
          this.showConfirmation = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    onUpdateReset(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      this.resetForm();
    },

    deleteTodo(todo) {
      const todoURL = dataURL + todo.uid;
      axios.delete(todoURL)
        .then(() => {
          this.getTodos();
          this.message = 'Задача удалена из списка';
          this.showConfirmation = true;
        })
        .catch((error) => {
          console.log(error);
        });
    },

  },

  components: {
    confirmation: Confirmation,
  },

  created() {
    this.getTodos();
  },

};
</script>

<style>
button#task-add, button#load-task, button#save-task {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.todo-uid {
  text-align: right;
}
</style>
