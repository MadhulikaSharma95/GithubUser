import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [users, setUsers] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedUserRepos, setSelectedUserRepos] = useState(null);

  const fetchAvailableUsers = async () => {
    const users = await fetch("http://localhost:8080/api/users").then((res) =>
      res.json()
    );
    console.log({ users });
    setUsers(users);
  };

  const fetchSelectedUserRepos = async () => {
    const usersRepos = await fetch(
      `http://localhost:8080/api/user/${selectedUser}`
    ).then((res) => res.json());

    console.log({ usersRepos });
    setSelectedUserRepos(usersRepos);
  };

  useEffect(() => {
    fetchAvailableUsers();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      console.log({ selectedUser });
      fetchSelectedUserRepos(selectedUser);
      console.log({ selectedUserRepos });
    }
  }, [selectedUser]);

  return (
    <div className="App" style={{ marginTop: "100px" }}>
      <h2>Select Github user:</h2>
      <select
        defaultValue=""
        value={selectedUser}
        onChange={(e) => setSelectedUser(e.target.value)}
      >
        <option disabled value="">
          Please select a user
        </option>
        {users?.map(({ username }) => (
          <option>{username}</option>
        ))}
      </select>
      {selectedUserRepos?.map((userRepo) => (
        <h4>{userRepo.name}</h4>
      ))}
    </div>
  );
}

export default App;
