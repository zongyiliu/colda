// console.log(" this.exe_position",  node_path.resolve("./resources/dist/run/run.exe"))
// console.log("dir",__dirname)
// console.log(node_path.join(__dirname, '../dist/run/run.exe'))
// import path from 'path'
// console.log("fs", fs)

console.log("54321")
// const Database = window.db
const Database = require('better-sqlite3');
console.log('21312312', Database)
const db = new Database('foobar.db', { verbose: console.log });
console.log('21312312', db)
// let db = 5


// const sqlite3 = window.require('sqlite3').verbose();
// const node_path = window.require('path');
// const fs = window.require("fs")
// console.log('dbadress', __dirname)

// function createDatabase(file){
//   console.log("file_position", file)
//   if(!fs.existsSync(file)){
    
//     console.log("creating database file");
//     fs.openSync(file, "w");
//     console.log("file created");
//   }

  // var db = new sqlite3.Database(
  //   file, 
  //   sqlite3.OPEN_READWRITE, 
  //   function (err) {
  //       if (err) {
  //           return console.log(err.message)
  //       }
  //       console.log('connect database successfully')
  //   }
  // )
  // return db

let db = createDatabase(node_path.join(__dirname,'../../Apollo_Client_data.db'))
console.log('position', __dirname)

// // let db = new sqlite3.Database('Apollo_Client_db');

db.serialize(function() {
  db.run("CREATE TABLE IF NOT EXISTS User_Default_Table (id                    int primary key, \
                                                   user_id                    int, \
                                                   default_train_file_path    text, \
                                                   default_train_id_column          text, \
                                                   default_train_data_column        text, \
                                                   default_train_target_column      text, \
                                                   mode                       text)");

  db.run("CREATE TABLE IF NOT EXISTS User_Sponsor_Table (id     int primary key, \
                                           task_name          text,\
                                           task_description   text,\
                                           user_id            int, \
                                           test_indicator     text, \
                                           task_id            text, \
                                           test_id            text, \
                                           train_file_path    text, \
                                           train_id_column    text, \
                                           train_data_column  text, \
                                           train_target_column text, \
                                           test_file_path     text, \
                                           test_id_column     text, \
                                           test_data_column   text, \
                                           test_target_column text, \
                                           task_mode          text, \
                                           model_name         text, \
                                           metric_name        text)");
// user manual
    db.run("CREATE TABLE IF NOT EXISTS User_Manual_Table (id                  int primary key, \
                                                   task_name                  text,\
                                                   task_description           text,\
                                                   user_id                    int, \
                                                   task_id                    text,\
                                                   test_id                    text,\
                                                   pending_train_file_path    text, \
                                                   pending_train_id_column          text, \
                                                   pending_train_data_column        text, \
                                                   pending_train_target_column      text, \
                                                   pending_test_file_path    text, \
                                                   pending_test_id_column          text, \
                                                   pending_test_data_column        text, \
                                                   pending_test_target_column      text)");
                                                   
                                         
                                           
// });
// let db=5;
console.log('db1',db)
export default db
// exports.default = db