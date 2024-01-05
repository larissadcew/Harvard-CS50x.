// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
 node;

// Choose number of buckets in hash table
const unsigned int N = 26;

// global variable
int word_count = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *words)
{
    // TODO
    int hash_value = hash(words);
    node *cursor = table[hash_value];

    // checking if the word is in the hash
    while (cursor != NULL)
    {
        if (strcasecmp(words, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *words)
{
    // Improve this hash function
    unsigned int total = 0;
    for (int i = 0; i < strlen(words); i++)
    {
        total += tolower(words[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }
    char words[LENGTH + 1];

    // reading all strings
    while (fscanf(file, "%s", words) != EOF)
    {
        // putting memory to a new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        // copying strings
        strcpy(n->word, words);
        int hash_value = hash(words);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        // if cursor not is NULL
        while (cursor)
        {
            node *tmp = cursor;
            free(cursor);
            cursor = cursor->next;
        }
        // if cursor is NULL
        if (cursor == NULL)
        {
            return true;
        }
    }
    return false;
}