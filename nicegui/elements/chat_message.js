export default {
  template: `
    <q-chat-message
      :text="text"
      :name="name"
      :label="label"
      :stamp="stamp"
      :avatar="avatar"
      :sent=sent
    />
  `,
  props: {
    text: Array,
    name: String,
    label: String,
    stamp: String,
    avatar: String,
    sent: Boolean,
  },
};
