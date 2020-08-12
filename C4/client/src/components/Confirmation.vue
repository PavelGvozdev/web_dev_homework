<template>
  <div>
    <b-alert variant="success"
            show
            dismissible
            @dismissed='onDismissed'
             >
            {{ message }}
    </b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],

  methods: {

    onDismissed() {
      this.$emit('dismissed');
    },

  },

};

</script>
