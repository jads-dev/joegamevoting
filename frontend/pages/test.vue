<template>
  <div>
    {{ can_vote }}
  </div>
</template>


<script>
export default {
  mounted: async function () {
    const response = await this.$axios.$get("/api/can_vote");
    this.can_vote = response;
  },
  data: () => ({
    can_vote: "",
  }),
};
</script>