import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/splash_screen.dart';
import 'screens/SearchScreen.dart';
import 'screens/SavedScreen.dart';
import 'screens/ProfileScreen.dart';
import 'screens/GalleryPage.dart';
import 'providers/app_provider.dart';
import 'models/outfit.dart';
import 'screens/Notify.dart';

// Paleta de colores de The Clothesure
class ClothesureColors {
  static const Color azul = Color(0xFF3BAEB0);
  static const Color rojo = Color(0xFFE23F58);
  static const Color amarillo = Color(0xFFF59153);
  static const Color negro = Color(0xFF000000);
}

void main() {
  runApp(const ClothesureApp());
}

class ClothesureApp extends StatelessWidget {
  const ClothesureApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AppProvider(),
      child: MaterialApp(
        title: 'The Clothesure',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: ClothesureColors.azul,
            brightness: Brightness.light,
            primary: ClothesureColors.azul,
            secondary: ClothesureColors.rojo,
            tertiary: ClothesureColors.amarillo,
            surface: Colors.grey[50],
          ),
          useMaterial3: true,
          fontFamily: 'Roboto',
          appBarTheme: const AppBarTheme(
            backgroundColor: ClothesureColors.negro,
            foregroundColor: Colors.white,
            elevation: 0,
            titleTextStyle: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
              fontFamily: 'Roboto',
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: ClothesureColors.azul,
              foregroundColor: Colors.white,
              textStyle: const TextStyle(
                fontFamily: 'Roboto',
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          bottomNavigationBarTheme: const BottomNavigationBarThemeData(
            backgroundColor: ClothesureColors.negro,
            selectedItemColor: ClothesureColors.azul,
            unselectedItemColor: Colors.white,
            type: BottomNavigationBarType.fixed,
          ),
        ),
        home: const SplashScreen(),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  final List<Widget> _screens = [
    const FeedScreen(),
    const SearchScreen(),
    const GalleryPage(),
    const ProfileScreen(),
    const SavedScreen(),
  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          border: Border(
            top: BorderSide(color: Color(0xFFE5E5E5), width: 0.5),
          ),
        ),
        child: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: (index) {
            setState(() {
              _selectedIndex = index;
            });
          },
        //color de la barra de navegacion
        type: BottomNavigationBarType.fixed,
        backgroundColor: ClothesureColors.negro,
        selectedItemColor: ClothesureColors.azul,
        unselectedItemColor: Colors.white,
          selectedLabelStyle:
              const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
          unselectedLabelStyle: const TextStyle(fontSize: 12),
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.home),
              activeIcon: Icon(Icons.home),
              label: '',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.search_outlined),
              activeIcon: Icon(Icons.search),
              label: '',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.add_circle_outline),
              activeIcon: Icon(Icons.add_circle),
              label: '',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.person),
              activeIcon: Icon(Icons.person),
              label: '',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.menu),
              activeIcon: Icon(Icons.menu),
              label: '',
            ),
          ],
        ),
      ),
    );
  }
}

//feeds
class FeedScreen extends StatefulWidget {
  const FeedScreen({super.key});

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  @override
  void initState() {
    super.initState();
    // Cargar outfits del feed al inicializar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AppProvider>().loadFeedOutfits();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Row(
          children: <Widget>[
            const Text(
              'CLOTHESURE',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.black,
                letterSpacing: 1.2,
              ),
            ),
            const Spacer(),
            SizedBox(
              width: 80,
              height: 55,
              child: IconButton(
                onPressed: () {
                  Navigator.push(context,
                    MaterialPageRoute(builder: (context) => const Notify()),
                  );
                },
                icon: Image.asset(
                  'assets/images/logo.png',
                  width: 50,
                  height: 40,
                ),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(2),
          child: Container(
            height: 8,
            color: ClothesureColors.rojo,
            /*child:const Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Progresscard(
                totalHooks: 1000,
                hooksLeft: 350,
                progressColor: Colors.teal,
              ),
              Progresscard(
                totalHooks: 1000,
                hooksLeft: 850,
                progressColor: Colors.red,
              ),
              Progresscard(
                totalHooks: 1000,
                hooksLeft: 150,
                progressColor: Colors.orange,
               ),
              ],
             ),*/
            ),
          ),
        ),
      
      body: Consumer<AppProvider>(
        builder: (context, appProvider, child) {
          if (appProvider.isLoading && appProvider.feedOutfits.isEmpty) {
            return const Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(
                  ClothesureColors.azul,
                ),
              ),
            );
          }
          if (appProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 64,
                    color: Color.fromARGB(255, 6, 3, 233),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Error: ${appProvider.error}',
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.red,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => appProvider.loadFeedOutfits(),
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          if (appProvider.feedOutfits.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.checkroom,
                    size: 64,
                    color: Color(0xFF8B1538),
                  ),
                  SizedBox(height: 16),
                  Text(
                    'No hay outfits disponibles',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF8B1538),
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Sé el primero en subir un outfit',
                    style: TextStyle(
                      fontSize: 14,
                      color: Color.fromARGB(255, 6, 32, 229),
                    ),
                  ),
                ],
              ),
            );
          }
          //Color del refresh
          return RefreshIndicator(
            onRefresh: () => appProvider.loadFeedOutfits(),
            color: ClothesureColors.azul,
            child: ListView.builder(
              itemCount: appProvider.feedOutfits.length,
              itemBuilder: (context, index) {
                final outfit = appProvider.feedOutfits[index];
                return _buildPostCard(
                  outfit: outfit,
                  onLike: () => appProvider.likeOutfit(outfit.id),
                  onUnlike: () => appProvider.unlikeOutfit(outfit.id),
                  onSave: () => appProvider.saveOutfit(outfit.id),
                  onUnsave: () => appProvider.unsaveOutfit(outfit.id),
                  onView: () => appProvider.recordOutfitView(outfit.id),
                );
              },
            ),
          );
        },
      ),
    );
  }
  Widget _buildPostCard({
    required Outfit outfit,
    required VoidCallback onLike,
    required VoidCallback onUnlike,
    required VoidCallback onSave,
    required VoidCallback onUnsave,
    required VoidCallback onView,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header del usuario
          Padding(
            padding: const EdgeInsets.all(12),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 18,
                  backgroundColor: ClothesureColors.azul,
                  backgroundImage: outfit.profileImage != null
                      ? NetworkImage(outfit.profileImage!)
                      : null,
                  child: outfit.profileImage == null
                      ? const Icon(Icons.person, color: Colors.white, size: 18)
                      : null,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        outfit.username ?? 'Usuario',
                        style: const TextStyle(
                          fontWeight: FontWeight.w600,
                          fontSize: 15,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text(
                        '@${outfit.userId}',
                        style: TextStyle(
                          color: Colors.grey[600],
                          fontSize: 13,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                Text(
                  _formatTimeAgo(outfit.createdAt),
                  style: TextStyle(
                    color: Colors.grey[500],
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),

          // Imagen del post
          Container(
            height: 250,
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.circular(8),
            ),
            child: outfit.mainImage.isNotEmpty
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      outfit.mainImage,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) =>
                          const Center(
                        child: Icon(
                          Icons.image_not_supported,
                          size: 60,
                          color: Colors.grey,
                        ),
                      ),
                    ),
                  )
                : const Center(
                    child: Icon(
                      Icons.checkroom,
                      size: 60,
                      color: Colors.grey,
                    ),
                  ),
          ),

          // Contenido del post
          Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  outfit.title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 6),
                Text(
                  outfit.description,
                  style: TextStyle(
                    color: Colors.grey[700],
                    fontSize: 13,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),

                // Hashtags
                if (outfit.hashtags.isNotEmpty)
                  Wrap(
                    spacing: 6,
                    runSpacing: 4,
                    children: outfit.hashtags
                        .take(3)
                        .map((tag) => Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: ClothesureColors.azul.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                tag,
                                style: TextStyle(
                                  color: ClothesureColors.azul,
                                  fontSize: 10,
                                  fontWeight: FontWeight.w500,
                                  fontFamily: 'Roboto',
                                ),
                              ),
                            ))
                        .toList(),
                  ),

                const SizedBox(height: 12),

                // Stats y acciones
                Row(
                  children: [
                    _buildStatItem(
                        Icons.visibility, _formatCount(outfit.viewsCount)),
                    const SizedBox(width: 16),
                    _buildStatItem(
                        Icons.comment, _formatCount(outfit.commentsCount)),
                    const SizedBox(width: 16),
                    GestureDetector(
                      onTap: outfit.isLiked ? onUnlike : onLike,
                      child: _buildStatItem(
                        outfit.isLiked ? Icons.favorite : Icons.favorite_border,
                        _formatCount(outfit.likesCount),
                        color: outfit.isLiked ? ClothesureColors.rojo : Colors.grey,
                      ),
                    ),
                    const Spacer(),
                    GestureDetector(
                      onTap: outfit.isSaved ? onUnsave : onSave,
                      child: Icon(
                        outfit.isSaved ? Icons.bookmark : Icons.bookmark_border,
                        color: outfit.isSaved
                            ? ClothesureColors.azul
                            : Colors.grey,
                        size: 20,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(IconData icon, String count, {Color? color}) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          icon,
          size: 14,
          color: color ?? Colors.grey[600],
        ),
        const SizedBox(width: 3),
        Text(
          count,
          style: TextStyle(
            color: color ?? Colors.grey[600],
            fontSize: 12,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  String _formatCount(int count) {
    if (count >= 1000000) {
      return '${(count / 1000000).toStringAsFixed(1)}M';
    } else if (count >= 1000) {
      return '${(count / 1000).toStringAsFixed(1)}k';
    } else {
      return count.toString();
    }
  }

  String _formatTimeAgo(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inDays > 0) {
      return 'hace ${difference.inDays} día${difference.inDays > 1 ? 's' : ''}';
    } else if (difference.inHours > 0) {
      return 'hace ${difference.inHours} hora${difference.inHours > 1 ? 's' : ''}';
    } else if (difference.inMinutes > 0) {
      return 'hace ${difference.inMinutes} minuto${difference.inMinutes > 1 ? 's' : ''}';
    } else {
      return 'ahora';
    }
  }
}
