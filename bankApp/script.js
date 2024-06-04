// BANKIST APP

// Data (Reperesented with arrays and Objects)
const account1 = {
  owner: 'Jonas Schmedtmann',
  movements: [200.0, 450, -400, 3000, -650, -130, 70, 1300],
  interestRate: 1.2, // %
  pin: 1111,

  movementsDates: [
    '2023-04-28T21:31:17.178Z',
    '2023-04-27T21:31:17.178Z',
    '2023-04-21T21:31:57.178Z',
    '2023-03-19T21:31:27.178Z',
    '2023-03-07T21:45:17.178Z',
    '2023-03-17T21:35:17.178Z',
    '2023-02-21T21:31:19.178Z',
    '2023-01-23T21:31:17.178Z',
  ],
  currency: 'EUR',
  locale: 'de-DE',
};

const account2 = {
  owner: 'Jessica Davis',
  movements: [5000, 3400, -150, -790, -3210, -1000, 8500, -30],
  interestRate: 1.5,
  pin: 2222,

  movementsDates: [
    '2019-11-01T13:15:33.035Z',
    '2019-11-30T09:48:16.867Z',
    '2019-09-15T06:04:23.907Z',
    '2020-01-25T14:18:46.235Z',
    '2020-02-05T16:33:06.386Z',
    '2020-04-10T14:43:26.374Z',
    '2020-06-25T18:49:59.371Z',
    '2020-07-26T12:01:20.894Z',
  ],
  currency: 'USD',
  locale: 'en-US',
};

const accounts = [account1, account2];

//////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////

// Getting all html elements via class and id attributes
const labelWelcome = document.querySelector('.welcome');
const labelDate = document.querySelector('.date');
const labelBalance = document.querySelector('.balance__value');
const labelSumIn = document.querySelector('.summary__value--in');
const labelSumOut = document.querySelector('.summary__value--out');
const labelSumInterest = document.querySelector('.summary__value--interest');
const labelTimer = document.querySelector('.timer');

const containerApp = document.querySelector('.app');
const containerMovements = document.querySelector('.movements');

const btnLogin = document.querySelector('.login__btn');
const btnTransfer = document.querySelector('.form__btn--transfer');
const btnLoan = document.querySelector('.form__btn--loan');
const btnClose = document.querySelector('.form__btn--close');
const btnSort = document.querySelector('.btn--sort');

const inputLoginUsername = document.querySelector('.login__input--user');
const inputLoginPin = document.querySelector('.login__input--pin');
const inputTransferTo = document.querySelector('.form__input--to');
const inputTransferAmount = document.querySelector('.form__input--amount');
const inputLoanAmount = document.querySelector('.form__input--loan-amount');
const inputCloseUsername = document.querySelector('.form__input--user');
const inputClosePin = document.querySelector('.form__input--pin');

/*
Calculate and display the dates of each transactions.
*/

const displayMovementDates = (date, locale) => {
  const howLongAgo = (date1, date2) => {
    return Math.round(Math.abs(date2 - date1) / (1000 * 60 * 60 * 24));
  };

  const length = howLongAgo(new Date(), date);

  const options = {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
    //hour: 'numeric',minute: 'numeric',second: 'numeric',timeZoneName: 'shortGeneric',
  };

  if (length === 0) return 'Today';
  if (length === 1) return 'Yesterday';
  if (length <= 7) return `${length} days ago`;
  else {
    // const day = `${date.getDate()}`.padStart(2, 0);
    // const month = `${date.getMonth() + 1}`.padStart(2, 0);
    // const year = date.getFullYear();
    // const hours = date.getHours();
    // const mins = `${date.getMinutes()}`.padStart(2, 0);
    // return `${month}/${day}/${year}`;
    return new Intl.DateTimeFormat(locale, options).format(date);
  }
};

/*
Empty all old transactions by setting the inner html to an empty string
Loop over all account transactiion movements (Deposit and Withdrawal) and
add new html for them on a new row.
Add new html as adjacent to the parent div (afterbegin of the parent)
*** other insertAdjacentHTML ***
<beforeBegin beforeEnd afterEnd> 
*/

const displayMovement = (acc, sort = false) => {
  containerMovements.innerHTML = '';

  const movs = sort
    ? acc.movements.slice().sort((a, b) => a - b)
    : acc.movements;

  movs.forEach(function (mov, index, array) {
    const type = mov > 0 ? 'deposit' : 'withdrawal';

    // Get the display dates for each transaction from the respective date strings in the acc obj
    const date = new Date(acc.movementsDates[index]);
    const display = displayMovementDates(date, acc.locale);

    const formattedValues = new Intl.NumberFormat(acc.locale, {
      style: 'currency',
      currency: acc.currency,
    }).format(mov);

    const html = `
         <div class="movements__row">
          <div class="movements__type movements__type--${type}">${
      index + 1
    } ${type}</div>
          <div class="movements__date">${display}</div>
          <div class="movements__value">${formattedValues}</div>
        </div>
        `;
    //<div class="movements__value">$${mov.toFixed(2)}</div>;
    containerMovements.insertAdjacentHTML('afterbegin', html);
  });
};

/*
Calculate current balance in account from different acc activities (movements)
Loop over all account transactiion movements (Deposit and Withdrawal) and
add return the current monentary value in the acc using the "REDUCE" method.
Add the value as textContent for the label
*/
const calcDisplayBalance = (acc) => {
  const balance = acc.movements.reduce((accumulator, mov) => {
    return accumulator + mov;
  }, 0);
  acc.balance = balance;
  const formattedBalance = Intl.NumberFormat(acc.locale, {
    style: 'currency',
    currency: acc.currency,
  }).format(acc.balance);
  labelBalance.textContent = `${formattedBalance}`;

  const date = new Date();
  const options = {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    timeZoneName: 'shortGeneric',
  };
  labelDate.textContent = new Intl.DateTimeFormat(
    navigator.language,
    options
  ).format(date);

  // const now = new Date();
  // const curr_day = `${now.getDate()}`.padStart(2, 0);
  // const curr_month = `${now.getMonth() + 1}`.padStart(2, 0);
  // const curr_year = now.getFullYear();
  // const curr_hours = now.getHours();
  // const curr_mins = `${now.getMinutes()}`.padStart(2, 0);

  // labelDate.textContent = `${curr_month}/${curr_day}/${curr_year}, ${curr_hours}:${curr_mins}`;
};

/*
Create usernames for each account by grabbing the first letters of the account's 
owner names. (First Middle Last) and add it as a new attribute for the account object.
*/
const createUsername = (accounts) => {
  accounts.forEach((acc) => {
    acc.username = acc.owner
      .toLowerCase()
      .split(' ')
      .map((name) => name[0])
      .join('');
  });
};

/*
Calculate all summary values (Incoming, Outgoing and total discounts accquired on deposits
Display calculated values in the appropriate html element position
This is donr using the Filter, Map, and Reduce methods of the array object
*/
const calcDisplaySummary = function (acc) {
  const incoming = acc.movements
    .filter((mov, i, arr) => {
      return mov > 0;
    })
    .reduce((acc, mov, i, arr) => {
      return acc + mov;
    }, 0);

  const outgoing = acc.movements
    .filter((mov) => mov < 0)
    .reduce((acc, mov) => {
      return acc + mov;
    }, 0);

  const interest = acc.movements
    .filter((mov) => mov > 0)
    .map((deposit) => deposit * (acc.interestRate / 100))
    .filter((intrestValue, i, arr) => {
      return intrestValue >= 1;
    })
    .reduce((accumulator, interest) => accumulator + interest, 0);

  labelSumIn.textContent = `${new Intl.NumberFormat(acc.locale, {
    style: 'currency',
    currency: acc.currency,
  }).format(incoming)}`;

  labelSumOut.textContent = `${new Intl.NumberFormat(acc.locale, {
    style: 'currency',
    currency: acc.currency,
  }).format(Math.abs(outgoing))}`;

  labelSumInterest.textContent = `${new Intl.NumberFormat(acc.locale, {
    style: 'currency',
    currency: acc.currency,
  }).format(interest)}`;
};

/*
Display Function:
Displays the accounts deposit and withdrawals (displayMovement)
Displays tht current account balance
Displays the Summary of all deposit, withdrawal and interest made.
*/
const displayInfo = (acc) => {
  // Display movements
  displayMovement(acc);

  // Display balance
  calcDisplayBalance(acc);

  // Display the account summary
  calcDisplaySummary(acc);
};

let currentAccount, timer;

// Fake always logged in
// currentAccount = account1;
// displayInfo(currentAccount);
// containerApp.style.opacity = 100;

// const num = 3000;
// const currencies = {
//   style: 'currency',
//   currency: 'EUR',
// };
// const content = Intl.NumberFormat('en-EU', currencies).format(num);
// console.log(content);
// console.log(
//   new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(
//     num
//   )
// );

// const day = `${date.getDate()}`.padStart(2, 0);
// const month = `${date.getMonth() + 1}`.padStart(2, 0);
// const year = date.getFullYear();
// const hours = date.getHours();
// const mins = `${date.getMinutes()}`.padStart(2, 0);

// labelDate.textContent = `${month}/${day}/${year}, ${hours}:${mins}`;
// console.log(`${month}/${day}/${year}, ${hours}:${mins}`);

// let time = 10;
// const tick = () => {
//   const min = String(Math.trunc(time / 60)).padStart(2, 0);
//   const sec = String(Math.trunc(time % 60)).padStart(2, 0);
//   console.log(`Current time is ${min}:${sec}`);
//   let currentTime = `${min}:${sec}`;

//   labelTimer.textContent = currentTime;
//   time--;

//   if (time === 0) {
//     clearInterval(timer);
//   }
// };

const startLogout = function () {
  const tick = () => {
    const min = String(Math.trunc(time / 60)).padStart(2, 0);
    const sec = String(Math.trunc(time % 60)).padStart(2, 0);
    console.log(`Current time is ${min}:${sec}`);
    let currentTime = `${min}:${sec}`;

    labelTimer.textContent = currentTime;

    if (time === 0) {
      clearInterval(timer);
      containerApp.style.opacity = '0';
      labelWelcome.textContent = `Log in to get started`;
    }

    time--;
  };

  // Set timer to 5 mins
  let time = 30;
  tick();
  const timer = setInterval(tick, 1000);
  return timer;
};

// const startLogout = function () {
//   // Set timer to 5 mins
//   let time = 10;

//   const timer = setInterval(() => {
//     const min = String(Math.trunc(time / 60)).padStart(2, 0);
//     const sec = String(Math.trunc(time % 60)).padStart(2, 0);
//     console.log(`Current time is ${min}:${sec}`);
//     let currentTime = `${min}:${sec}`;

//     labelTimer.textContent = currentTime;
//     time--;

//     if (time === 0) {
//       clearInterval(timer);
//     }
//   }, 1000);

//   setTimeout(() => {
//     console.log(`Here in setTimeout`);
//     console.log(`Calling the logout function now!!!`);
//     containerApp.style.opacity = '0';
//     labelWelcome.textContent = `Log in to get started`;
//   }, 11000);
// };

/*
Login:
On button click, fire the event to get the login credentials and display account info
Check to see if account username matches any in the accounts array (array of acc objects)
Check the pin associated with the acc and validate it matches with the inputed pin value

Display account details (Balance, transactions) once login has been successful
*/

btnLogin.addEventListener('click', function (e) {
  e.preventDefault();

  currentAccount = accounts.find(
    (acc) => acc.username === inputLoginUsername.value
  );

  if (currentAccount && currentAccount.pin === Number(inputLoginPin.value)) {
    labelWelcome.textContent = `Welcome back ${
      currentAccount.owner.split(' ')[0]
    }`;
    // If we get valid user, clear input field and display necessary info.
    inputLoginUsername.value = '';
    inputLoginPin.value = '';

    // Start logout Countdown
    if (timer) clearInterval(timer);
    timer = startLogout();

    // update current account's UI with new information
    displayInfo(currentAccount);
    containerApp.style.opacity = '100';
  }
});

/*
Login:
On button click, fire the event to get the receivers credentials and transfer amount
Check to see if receiver account username matches any in the accounts array (array of acc objects)
Check to see if transfer amount is valid (Within possible transfer limit)

Update senders and receivers account
Update the UI to display changes.
*/
btnTransfer.addEventListener('click', function (e) {
  e.preventDefault();

  const receiverName = inputTransferTo.value;
  const receiverAccount = accounts.find((acc) => acc.username === receiverName);
  const transferAmount = Number(inputTransferAmount.value);

  inputTransferTo.value = inputTransferAmount.value = '';

  if (
    transferAmount > 0 &&
    transferAmount <= currentAccount.balance &&
    receiverAccount &&
    receiverAccount.username !== currentAccount.username
  ) {
    // Remove amount from sender account and update the date of transaction
    currentAccount.movements.push(transferAmount * -1);
    currentAccount.movementsDates.push(new Date().toISOString());

    // Add to receiver account and update the date of transaction
    receiverAccount.movements.push(transferAmount);
    receiverAccount.movementsDates.push(new Date().toISOString());

    // update current account's UI with new information
    displayInfo(currentAccount);

    // Reset  Timer
    clearInterval(timer);
    timer = startLogout();
  }
});

/*
Close Account:
On button click, fire the event to get the User credentials (username and pin) and verify the
username entered is the current user.
*/
btnClose.addEventListener('click', (e) => {
  e.preventDefault();

  const user = inputCloseUsername.value;

  if (
    currentAccount.username === user &&
    currentAccount.pin === Number(inputClosePin.value)
  ) {
    const userIndex = accounts.findIndex((acc) => {
      return acc.username === user;
    });
    console.log(accounts.length);
    accounts.splice(userIndex, 1);

    inputCloseUsername.value = '';
    inputClosePin.value = '';
    console.log(accounts.length);

    // Hide UI
    containerApp.style.opacity = 0;
  }
});

btnLoan.addEventListener('click', function (e) {
  e.preventDefault();

  const amount = Math.floor(inputLoanAmount.value);

  if (
    amount > 0 &&
    currentAccount.movements.some((mov) => mov >= amount * 0.1)
  ) {
    setTimeout(function () {
      // Add movement and update the date of loan grant
      currentAccount.movements.push(amount);
      currentAccount.movementsDates.push(new Date().toISOString());

      // Update UI
      displayInfo(currentAccount);

      // Reset timer
      clearInterval(timer);
      timer = startLogOutTimer();
    }, 2500);
  }
  inputLoanAmount.value = '';
});

let sorted = false;
btnSort.addEventListener('click', function (e) {
  e.preventDefault();
  displayMovement(currentAccount, !sorted);
  sorted = !sorted;
});

createUsername(accounts);

////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////

// Numbers

// console.log(Number.parseInt('256'));
// const num = Math.floor(Math.random() * (10 - 1 + 1) + 1);
// console.log(num);

// const randomInt = (min, max) =>
//   Math.floor(Math.random() * (max - min) + 1) + min;
// console.log(randomInt(1, 10));

// console.log(2 ** 53 - 1);
// console.log(Number.MAX_SAFE_INTEGER);
// console.log(Number.MAX_VALUE);
// console.log(Number.MIN_VALUE);

// Date and Time.

// const date2 = new Date('April 27, 2023');
// const date3 = new Date(3 * 24 * 60 * 60 * 1000);

// const future = new Date(2037, 10, 19, 15, 23);
// console.log(future);
// console.log(future.toISOString());
// console.log(future.toDateString());
// console.log(future.toTimeString());
