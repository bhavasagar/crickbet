import moment from 'moment';
const formatDateTime = (date) => moment.utc(date).local().format('MMM, DD YYYY h:mm A');
export default formatDateTime;