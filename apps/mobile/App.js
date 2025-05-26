import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList } from 'react-native';

export default function App() {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/sessions/today')
      .then((res) => res.json())
      .then((data) => setSessions(data));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mes séances du jour</Text>
      <FlatList
        data={sessions}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Text>{item.sport} - {item.duration_min} min</Text>
        )}
      />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 50,
  },
  title: {
    fontSize: 20,
    marginBottom: 20,
  },
});
