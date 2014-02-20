
SDL_INCLUDE = -IC:/MinGW/include
SDL_LIB = -LC:/MinGW/lib -lSDL2main -lSDL2
# GL_INCLUDE = 
GL_LIB = -lopengl32 -lglu32

COMPILER = g++
COMPILER_FLAGS = -Wall -c -g -std=c++11 $(SDL_INCLUDE)
LD_FLAGS = -lmingw32 -mwindows -mconsole -std=c++11 $(GL_LIB) $(SDL_LIB)

all: cloud.exe

cloud.exe: cloud.o
	$(COMPILER) cloud_example.cpp cloud.o $(LD_FLAGS) -o $@

cloud.o: cloud.cpp cloud.h
	$(COMPILER) $(COMPILER_FLAGS) cloud.cpp -o $@

clean:
	rm *.o