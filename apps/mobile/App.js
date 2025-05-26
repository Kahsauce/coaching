import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View, FlatList } from 'react-native';

export default function App() {
  const sessions = [
    { id: '1', sport: 'Course', duration: 60 },
    { id: '2', sport: 'Vélo', duration: 90 },
  ];

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Mes séances du jour</Text>
      <FlatList
        data={sessions}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Text>{item.sport} - {item.duration} min</Text>
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
