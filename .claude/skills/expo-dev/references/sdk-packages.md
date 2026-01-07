# Expo SDK Packages Reference

Common SDK packages with usage patterns.

## expo-camera

```typescript
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';

export default function Camera() {
  const [facing, setFacing] = useState<CameraType>('back');
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  if (!permission?.granted) {
    return <Button title="Grant Permission" onPress={requestPermission} />;
  }

  const takePicture = async () => {
    const photo = await cameraRef.current?.takePictureAsync();
    console.log(photo?.uri);
  };

  return (
    <CameraView ref={cameraRef} style={{ flex: 1 }} facing={facing}>
      <Button title="Flip" onPress={() => setFacing(f => f === 'back' ? 'front' : 'back')} />
      <Button title="Take Photo" onPress={takePicture} />
    </CameraView>
  );
}
```

**Plugin config** (app.json):
```json
{ "plugins": [["expo-camera", { "cameraPermission": "Allow camera access" }]] }
```

## expo-image-picker

```typescript
import * as ImagePicker from 'expo-image-picker';

const pickImage = async () => {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images'],
    allowsEditing: true,
    aspect: [4, 3],
    quality: 1,
  });

  if (!result.canceled) {
    console.log(result.assets[0].uri);
  }
};

const takePhoto = async () => {
  const result = await ImagePicker.launchCameraAsync({
    allowsEditing: true,
    quality: 0.8,
  });
};
```

## expo-notifications

```typescript
import * as Notifications from 'expo-notifications';
import { useEffect, useRef, useState } from 'react';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export function useNotifications() {
  const [expoPushToken, setExpoPushToken] = useState<string>();
  const notificationListener = useRef<Notifications.EventSubscription>();

  useEffect(() => {
    registerForPushNotifications().then(token => setExpoPushToken(token));

    notificationListener.current = Notifications.addNotificationReceivedListener(notification => {
      console.log(notification);
    });

    return () => notificationListener.current?.remove();
  }, []);

  return expoPushToken;
}

async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return;

  const token = await Notifications.getExpoPushTokenAsync({ projectId: 'your-project-id' });
  return token.data;
}

// Schedule local notification
await Notifications.scheduleNotificationAsync({
  content: { title: 'Reminder', body: 'Check your tasks!' },
  trigger: { seconds: 60 },
});
```

## expo-location

```typescript
import * as Location from 'expo-location';

const getLocation = async () => {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') return;

  const location = await Location.getCurrentPositionAsync({});
  console.log(location.coords.latitude, location.coords.longitude);
};

// Background location
const startBackgroundLocation = async () => {
  await Location.requestBackgroundPermissionsAsync();

  await Location.startLocationUpdatesAsync('LOCATION_TASK', {
    accuracy: Location.Accuracy.Balanced,
    distanceInterval: 100,
  });
};
```

**Plugin config**:
```json
{
  "plugins": [
    ["expo-location", {
      "locationAlwaysAndWhenInUsePermission": "Allow location access"
    }]
  ]
}
```

## expo-secure-store

```typescript
import * as SecureStore from 'expo-secure-store';

// Store value
await SecureStore.setItemAsync('token', 'secret-value');

// Retrieve value
const token = await SecureStore.getItemAsync('token');

// Delete value
await SecureStore.deleteItemAsync('token');
```

## expo-file-system

```typescript
import * as FileSystem from 'expo-file-system';

// Read file
const content = await FileSystem.readAsStringAsync(FileSystem.documentDirectory + 'file.txt');

// Write file
await FileSystem.writeAsStringAsync(FileSystem.documentDirectory + 'file.txt', 'Hello World');

// Download file
const download = FileSystem.createDownloadResumable(
  'https://example.com/file.pdf',
  FileSystem.documentDirectory + 'file.pdf'
);
const result = await download.downloadAsync();

// File info
const info = await FileSystem.getInfoAsync(FileSystem.documentDirectory + 'file.txt');
console.log(info.exists, info.size);

// Delete file
await FileSystem.deleteAsync(FileSystem.documentDirectory + 'file.txt');
```

**Directories**:
- `FileSystem.documentDirectory` - Persistent storage
- `FileSystem.cacheDirectory` - Temporary cache
- `FileSystem.bundleDirectory` - Read-only bundled assets

## expo-image

High-performance image component (replaces `<Image>`):

```typescript
import { Image } from 'expo-image';

<Image
  source={{ uri: 'https://example.com/image.jpg' }}
  placeholder={blurhash}
  contentFit="cover"
  transition={200}
  style={{ width: 200, height: 200 }}
/>
```

**Props**:
- `contentFit`: `'cover' | 'contain' | 'fill' | 'scale-down'`
- `placeholder`: blurhash string or local asset
- `transition`: fade-in duration (ms)
- `cachePolicy`: `'memory' | 'disk' | 'memory-disk' | 'none'`

## expo-font

```typescript
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';

SplashScreen.preventAutoHideAsync();

export default function App() {
  const [fontsLoaded] = useFonts({
    'CustomFont': require('./assets/fonts/CustomFont.ttf'),
    'CustomFont-Bold': require('./assets/fonts/CustomFont-Bold.ttf'),
  });

  useEffect(() => {
    if (fontsLoaded) SplashScreen.hideAsync();
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return <Text style={{ fontFamily: 'CustomFont' }}>Hello</Text>;
}
```

## expo-haptics

```typescript
import * as Haptics from 'expo-haptics';

// Impact feedback
await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);

// Notification feedback
await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);

// Selection feedback
await Haptics.selectionAsync();
```

## expo-av (Audio/Video)

```typescript
import { Audio, Video } from 'expo-av';

// Audio playback
const { sound } = await Audio.Sound.createAsync(require('./audio.mp3'));
await sound.playAsync();

// Video component
<Video
  source={{ uri: 'https://example.com/video.mp4' }}
  useNativeControls
  resizeMode="contain"
  shouldPlay
  style={{ width: 300, height: 200 }}
/>
```
